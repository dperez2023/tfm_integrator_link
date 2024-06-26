import asyncio
import os
from datetime import datetime

from tapo import ApiClient
from tapo.requests import EnergyDataInterval

from enum import Enum
from pydantic import BaseModel

class DataFrequency(str, Enum):
    hourly = 'hourly'
    daily = 'daily'
    monthly = 'monthly'

class DataFrequencyModel(BaseModel):
    name: DataFrequency

class EnergyManager:
    async def authenticate(self, username):
        tapo_username = username
        tapo_password = "jaqrIk-xemwem-terxe6"
        ip_address = "192.168.1.129"

        client = ApiClient(tapo_username, tapo_password)
        device = await client.p110(ip_address)
        return device

    async def showDeviceInfo(self, device) :
        device_info = await device.get_device_info()
        print(f"Device info: {device_info.to_dict()} \n\n")

        device_usage = await device.get_device_usage()
        print(f"Device usage: {device_usage.to_dict()} \n\n")

        current_power = await device.get_current_power()
        print(f"Current power: {current_power.to_dict()} \n\n")

        energy_usage = await device.get_energy_usage()
        print(f"Energy usage: {energy_usage.to_dict()} \n\n")

    async def showEnergyData(self, device, format: str) -> str:
        today = datetime.today()

        if(format == DataFrequency.hourly):
            energy_data_hourly = await device.get_energy_data(
                EnergyDataInterval.Hourly,
                today)
            return energy_data_hourly.to_dict()
        elif(format == DataFrequency.daily):
            energy_data_daily = await device.get_energy_data(
                EnergyDataInterval.Daily,
                datetime(today.year, 3 * ((today.month - 1) // 3) + 1, 1),)
            return energy_data_daily.to_dict()
        elif(format == DataFrequency.monthly):
            energy_data_monthly = await device.get_energy_data(
                EnergyDataInterval.Monthly,
                datetime(today.year, 1, 1),)
            return energy_data_monthly.to_dict()
        else:
            return 'Incorrect EnergyDataInterval'