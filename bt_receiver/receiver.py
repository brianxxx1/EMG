import asyncio

from bleak import BleakClient, BleakScanner, BLEDevice
from car_control import CarControllingAgent

# from receiver import car_controlling_agent
# from receiver import signal_start
# import daemon
import threading
import time
# TODO: Add comments for below
service = "19B10000-E8F2-537E-4F6C-D104768A1214"
left_char_uuid = "19B10000-E8F2-537E-4F6C-D104768A1214"
right_char_uuid = "19B10000-E8F2-537E-4F6C-D104768A1215"
# Arduino is sending the EMG readings every 40 ms.
# So, 25 groups of readings per second are received in here.
# TODO: We may need to tune the activate threshold to have a good muscle activation detection.
global car_controlling_agent
car_controlling_agent = CarControllingAgent(voting_num=25, activate_threshold=0.3)


# def do_something():
#     while True:
#         if signal_start:
#             car_controlling_agent.refresh_car_action()
#         else:
#             car_controlling_agent.stop_car()

# def init_daemon():
#     with daemon.DaemonContext():
#         do_something()

# Create an Event object to control the thread's behavior
signal_start= threading.Event()

def do_something():
    global car_controlling_agent
    global signal_start
    while True:
        if signal_start.is_set():
            car_controlling_agent.refresh_car_action()
        else:
            car_controlling_agent.stop_car()

def init_thread(car_controlling_agent):
    thread = threading.Thread(target=do_something)
    thread.daemon = True  # Optional: Set it as a daemon thread if you want it to automatically close with the main program
    thread.start()
    return thread

    # Start the thread
    
car_thread = init_thread(car_controlling_agent)

# TODO: We may want a new main which is not async and waiting for readings.
time.sleep(1)
# If we are using this async main as our main control and we lose the bluetooth connection,
# the refresh car action will also wait for next reading. In other words, the car will not stop if
# we lose the bluetooth connection.
# Design a new main, call the receiver to get the readings and fill them into the voting_agent.
# A stand along damon process to refresh car_action. If we lose bluetooth connection, we set
# voting result of voting_agent to stop, and call refresh_car_action to stop the car.

signal_start.set()

async def main():
    my_device = "DC:54:75:C5:50:4D"
    # devices: list[BLEDevice] = await BleakScanner.discover()
    # print(devices)
    
    # for d in devices:
    #     print(d)
    #     # print(d.details)
    #     if d.details["props"].get("Name") == "EMG":
    #         my_device = d
    #         print("Found it")
    #         break

    async with BleakClient(my_device) as client:
        
        while True:
            left_reading = await client.read_gatt_char(left_char_uuid)
            left_reading = int.from_bytes(left_reading, byteorder='big')
            print(f"Left Reading is {left_reading}")
            right_reading = await client.read_gatt_char(right_char_uuid)
            right_reading = int.from_bytes(right_reading, byteorder='big')
            print(f"Right Reading is {right_reading}")

            # voting and taking car action based on voting result
            car_controlling_agent.fill_readings(
                left_reading=left_reading, right_reading=right_reading
            )
            
            car_controlling_agent.vote()
            car_controlling_agent.refresh_car_action()


asyncio.run(main())
