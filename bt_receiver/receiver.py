import asyncio

from bleak import BleakClient, BleakScanner, BLEDevice
from car_control import CarControllingAgent

# from receiver import car_controlling_agent
# from receiver import signal_start
# import daemon
import threading
import time
from datetime import datetime
import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# from test_swim import light_specific_leds

# TODO: Add comments for below
service = "19B10000-E8F2-537E-4F6C-D104768A1214"
left_char_uuid = "19B10000-E8F2-537E-4F6C-D104768A1214"
right_char_uuid = "19B10000-E8F2-537E-4F6C-D104768A1215"
# Arduino is sending the EMG readings every 40 ms.
# So, 25 groups of readings per second are received in here.
# TODO: We may need to tune the activate threshold to have a good muscle activation detection.
global car_controlling_agent
car_controlling_agent = CarControllingAgent(voting_num=3)


# plt.ion()  # Interactive mode on for dynamic plot updates
times = []
left_hand_emg = []
right_hand_emg = []

# def update(frame):
#     global times, left_hand_emg, right_hand_emg
#     # Update the plot
#     plt.cla()
#     plt.plot(times, left_hand_emg, label='Left Hand')
#     plt.plot(times, right_hand_emg, label='Right Hand')
#     plt.xlabel('Time (s)')
#     plt.ylabel('EMG Value')
#     plt.title('Real-time EMG Data')
#     plt.legend()
        
# Create an Event object to control the thread's behavior

# signal_start= threading.Event()

# def do_something():
#     global car_controlling_agent
#     global signal_start
#     while True:
#         time.sleep(1)
#         if signal_start.is_set():
#             car_controlling_agent.refresh_car_action()
#         # else:
#         #     car_controlling_agent.stop_car()

# def init_thread(car_controlling_agent):
#     thread = threading.Thread(target=do_something)
#     thread.daemon = True  # Optional: Set it as a daemon thread if you want it to automatically close with the main program
#     thread.start()
#     return thread

    # Start the thread


# TODO: We may want a new main which is not async and waiting for readings.
# time.sleep(1)
# If we are using this async main as our main control and we lose the bluetooth connection,
# the refresh car action will also wait for next reading. In other words, the car will not stop if
# we lose the bluetooth connection.
# Design a new main, call the receiver to get the readings and fill them into the voting_agent.
# A stand along damon process to refresh car_action. If we lose bluetooth connection, we set
# voting result of voting_agent to stop, and call refresh_car_action to stop the car.


def map_signal_to_led_index(signal, min_value, max_value, is_left):
    # Map the signal value from the range (min_value, max_value) to the LED index range
    if is_left:
        # Map to lower half (0-9)
        led_index = int(map_value(signal, min_value, max_value, 0, 9))
    else:
        # Map to upper half (11-20)
        led_index = int(map_value(signal, min_value, max_value, 11, 20))
    
    return led_index

def map_value(value, in_min, in_max, out_min, out_max):
    # Map a value from one range to another
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


async def main():
    # simple Mac Set up
    my_device = "DC:54:75:C5:50:4D"
    
    # crowded space
    # my_device = "3C98A56C-C1C7-A508-5508-058C45A0528F"
    # my_device = ""
    # devices: list[BLEDevice] = await BleakScanner.discover()
    # print(devices)
    
    # for d in devices:
    #     print(d)
    #     # print(d.details)
    #     if d.details["props"].get("Name") == "EMG":
    #         my_device = d
    #         print("Found it")
    #         break

    # method 1:
    def calculate_thresholds1(readings):
        # Calculate the threshold as a percentage of the maximum value
        # Adjust the percentage as needed
        threshold_percentage = 0.5
        max_reading = max(readings)
        min_reading = min(readings)

        return (max_reading+min_reading) * threshold_percentage
    
    # method 2:
    def calculate_thresholds2(readings, lower_percentile=5, upper_percentile=95):
        
        # Calculate the lower and upper bounds for filtering
        lower_bound = np.percentile(readings, lower_percentile)
        upper_bound = np.percentile(readings, upper_percentile)

        # Filter out the outliers
        filtered_data = [x for x in readings if lower_bound <= x <= upper_bound]

        # Calculate the mean of the filtered data
        mean_filtered = np.mean(filtered_data) if filtered_data else 0
        
        max_data = max(filtered_data)
        min_data = min(filtered_data)
        # or mean of max and min?
        # mean_filtered = np.mean([max(filtered_data), min(filtered_data)]) if filtered_data else 0
        return mean_filtered, max_data, min_data

    async with BleakClient(my_device) as client:
        
        # Calibration phase - collect data for 5 seconds
        calibration_data_left = []
        calibration_data_right = []
        print("Initiate Calibrating")
        start_time = time.time()
        while time.time() - start_time < 10:
            left_reading = await client.read_gatt_char(left_char_uuid)
            right_reading = await client.read_gatt_char(right_char_uuid)
            left_reading = int.from_bytes(left_reading, byteorder='big')
            right_reading = int.from_bytes(right_reading, byteorder='big')
            calibration_data_left.append(left_reading)
            calibration_data_right.append(right_reading)
            
            
            
        # Determine thresholds based on calibration data
        # use method1
        # left_threshold = calculate_thresholds1(calibration_data_left)
        # right_threshold = calculate_thresholds1(calibration_data_right)
        # use metho 2
        left_threshold, left_max, left_min = calculate_thresholds2(calibration_data_left)
        right_threshold, right_max, right_min = calculate_thresholds2(calibration_data_right)

        
        car_controlling_agent.activate_threshold_left = left_threshold
        car_controlling_agent.activate_threshold_right = right_threshold

        # print(calibration_data_left,"left" , "Threashold", left_threshold)
        # print(calibration_data_right,"right", "Threashold", right_threshold)
        
        # car_thread = init_thread(car_controlling_agent)

        # signal_start.set()
        print("finish Calibrating")
        while True:
    
            left_reading = await client.read_gatt_char(left_char_uuid)
            left_reading = int.from_bytes(left_reading, byteorder='big')
            # print(f"Left Reading is {left_reading}.{datetime.now()}")
            right_reading = await client.read_gatt_char(right_char_uuid)
            right_reading = int.from_bytes(right_reading, byteorder='big')
            # print(f"Right Reading is {right_reading}.{datetime.now()}")
            # voting and taking car action based on voting result
            
            # if left_reading >= left_threshold:
            #     if right_reading >= right_threshold:
            #         print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            #     else:
            #         print("<<<<<<<<<<<<<<-------------")
            # else:
            #     if right_reading >= right_threshold:
            #         print("--------------->>>>>>>>>>>>")
            #     else:
            #         print("Stop")
                    
            # left_hand_emg.append(left_reading)
            # right_hand_emg.append(right_hand_emg)
            # times.append(datetime.now())
            # ani = FuncAnimation(plt.gcf(), update, interval=100)
            # plt.tight_layout()
            # plt.show()
            # light up LEDs according to left_reading and right_reading
            
            # left_led_index = map_signal_to_led_index(left_reading, left_min, left_max, is_left=True)
            # right_led_index = map_signal_to_led_index(right_reading, right_min, right_max, is_left=False)
            
            # light_specific_leds(left_led_index,right_led_index)
            car_controlling_agent.fill_readings(
                left_reading=left_reading, right_reading=right_reading
            )
            
            car_controlling_agent.vote()
            
            
            
            # car_controlling_agent.refresh_car_action()


asyncio.run(main())
