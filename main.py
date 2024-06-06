import asyncio
import os
from datetime import datetime

from tapo import ApiClient
from tapo.requests import EnergyDataInterval

from enum import Enum

class DataFrequency(Enum):
    Hourly = 1
    Daily = 2
    Monthly = 3

DataFrequency = Enum('DataFrequency', ['Hourly', 'Daily', 'Monthly'])

async def main():
    tapo_username = "mfkzen@gmail.com"
    tapo_password = "jaqrIk-xemwem-terxe6"
    ip_address = "192.168.1.129"

    client = ApiClient(tapo_username, tapo_password)
    device = await client.p110(ip_address)
    return device

async def showDeviceInfo(device) :
    device_info = await device.get_device_info()
    print(f"Device info: {device_info.to_dict()} \n\n")

    device_usage = await device.get_device_usage()
    print(f"Device usage: {device_usage.to_dict()} \n\n")

    current_power = await device.get_current_power()
    print(f"Current power: {current_power.to_dict()} \n\n")

    energy_usage = await device.get_energy_usage()
    print(f"Energy usage: {energy_usage.to_dict()} \n\n")

async def showEnergyData(device, format: DataFrequency):
    switcher = {
        1: format == DataFrequency.Daily,
        2: format == DataFrequency.Hourly,
        3: format == DataFrequency.Monthly,
    }
    
    today = datetime.today()

    energy_data_hourly = await device.get_energy_data(EnergyDataInterval.Hourly, today)
    print(f"Energy data (hourly): {energy_data_hourly.to_dict()} \n\n")

    energy_data_daily = await device.get_energy_data(
        EnergyDataInterval.Daily,
        datetime(today.year, get_quarter_start_month(today), 1),
    )
    print(f"Energy data (daily): {energy_data_daily.to_dict()} \n\n")

    energy_data_monthly = await device.get_energy_data(
        EnergyDataInterval.Monthly,
        datetime(today.year, 1, 1),
    )
    print(f"Energy data (monthly): {energy_data_monthly.to_dict()} \n\n")

def get_quarter_start_month(today: datetime) -> int:
    return 3 * ((today.month - 1) // 3) + 1

async def run():
    device = await main()
    await showDeviceInfo(device)
    await showEnergyData(device, DataFrequency.Hourly)
    
if __name__ == "__main__":
    asyncio.run(run())