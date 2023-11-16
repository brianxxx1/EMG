import asyncio
from bleak import BleakScanner, BleakClient, BLEDevice
import voting

# TODO: Add comments for below
service = "19B10000-E8F2-537E-4F6C-D104768A1214"
left_char_uuid = "19B10000-E8F2-537E-4F6C-D104768A1214"
right_char_uuid = "19B10000-E8F2-537E-4F6C-D104768A1215"




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
        if d.details["props"].get("Name") == 'EMG':
            my_device = d
            print('Found it')
            break

    async with BleakClient(my_device) as client:
        LeftBuffer, RightBuffer = [], []
        while True:
            left_reading = await client.read_gatt_char(left_char_uuid)
            print(f"Left Reading is {int.from_bytes(left_reading, byteorder='big')}")
            right_reading = await client.read_gatt_char(right_char_uuid)
            print(f"Right Reading is {int.from_bytes(right_reading, byteorder='big')}")
            # vote
            voting.fill(LeftBuffer, left_reading, RightBuffer, right_reading)
            voting.vote(LeftBuffer, RightBuffer)

asyncio.run(main())
