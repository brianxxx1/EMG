import asyncio

from bleak import BleakClient, BleakScanner, BLEDevice
from car_control import CarControllingAgent

# TODO: Add comments for below
service = "19B10000-E8F2-537E-4F6C-D104768A1214"
left_char_uuid = "19B10000-E8F2-537E-4F6C-D104768A1214"
right_char_uuid = "19B10000-E8F2-537E-4F6C-D104768A1215"


# Arduino is sending the EMG readings every 40 ms.
# So, 25 groups of readings per second are received in here.
# TODO: We may need to tune the activate threshold to have a good muscle activation detection.
car_controlling_agent = CarControllingAgent(voting_num=25, activate_threshold=0.3)


# TODO: We may want a new main which is not async and waiting for readings.
# If we are using this async main as our main control and we lose the bluetooth connection,
# the refresh car action will also wait for next reading. In other words, the car will not stop if
# we lose the bluetooth connection.
# Design a new main, call the receiver to get the readings and fill them into the voting_agent.
# A stand along damon process to refresh car_action. If we lose bluetooth connection, we set
# voting result of voting_agent to stop, and call refresh_car_action to stop the car.
async def main():
    my_device = None
    devices: list[BLEDevice] = await BleakScanner.discover()
    print(devices)
    for d in devices:
        print(d.details)
        if d.details["props"].get("Name") == "EMG":
            my_device = d
            print("Found it")
            break

    async with BleakClient(my_device) as client:
        while True:
            left_reading = await client.read_gatt_char(left_char_uuid)
            print(f"Left Reading is {int.from_bytes(left_reading, byteorder='big')}")
            right_reading = await client.read_gatt_char(right_char_uuid)
            print(f"Right Reading is {int.from_bytes(right_reading, byteorder='big')}")

            # voting and taking car action based on voting result
            car_controlling_agent.fill_readings(
                left_reading=left_reading, right_reading=right_reading
            )
            car_controlling_agent.vote()
            car_controlling_agent.refresh_car_action()


asyncio.run(main())
