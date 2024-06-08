import asyncio
import os
from datetime import datetime

from tapo import ApiClient
from tapo.requests import EnergyDataInterval

from enum import Enum

DataFrequency = Enum('DataFrequency', ['Hourly', 'Daily', 'Monthly'])

class EnergyManager:
    async def authenticate(self, username):
        tapo_username = username
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

    async def showEnergyData(self, device, format: EnergyDataInterval) -> str:
        today = datetime.today()

        if(format == DataFrequency.Hourly):
            energy_data_hourly = await device.get_energy_data(format,
                                                              today)
            return energy_data_hourly.to_dict()
        elif(format == DataFrequency.Daily):
            energy_data_daily = await device.get_energy_data(
                format,
                datetime(today.year, 3 * ((today.month - 1) // 3) + 1, 1),)
            return energy_data_daily.to_dict()
        elif(format == DataFrequency.Monthly):
            energy_data_monthly = await device.get_energy_data(
                format,
                datetime(today.year, 1, 1),)
            return energy_data_monthly.to_dict()
        else:
            return 'Incorrect EnergyDataInterval'