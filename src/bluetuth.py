import asyncio
from bleak import BleakScanner
from bleak import BleakClient
async def scan():
    print("מחפש מכשירים...")
    devices = await BleakScanner.discover()
    for d in devices:
        print(f"שם: {d.name}, כתובת: {d.address}")

asyncio.run(scan())




DEVICE_ADDRESS = "הכתובת של המכשיר שלך"
CHARACTERISTIC_UUID = "ה־UUID של הערוץ המשדר נתונים"

def handle_data(sender, data):
    print(f"נתונים התקבלו: {data}")

async def connect():
    async with BleakClient(DEVICE_ADDRESS) as client:
        print("מחובר!")
        await client.start_notify(CHARACTERISTIC_UUID, handle_data)
        await asyncio.sleep(30)  # מאזין לנתונים 30 שניות
        await client.stop_notify(CHARACTERISTIC_UUID)

asyncio.run(connect())
