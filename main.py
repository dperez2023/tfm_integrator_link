#from PyP100 import PyP110
#p110 = PyP110.P110("192.168.1.129", "mfkzen@gmail.com", "jaqrIk-xemwem-terxe6") #Creates a P100 plug object

#p110.handshake() #Creates the cookies required for further methods
#p110.login() #Sends credentials to the plug and creates AES Key and IV for further methods

#The P110 has all the same basic functions as the plugs and additionally allow for energy monitoring.
#p110.getEnergyUsage() #Returns dict with all of the energy usage of the connected plug

#client = ApiClient("mfkzen@gmail.com", "jaqrIk-xemwem-terxe6")
#device = await client.p110("192.168.1.129")

import asyncio
import os
from datetime import datetime

from tapo import ApiClient
from tapo.requests import EnergyDataInterval

async def main():
    tapo_username = "mfkzen@gmail.com"
    tapo_password = "jaqrIk-xemwem-terxe6"
    ip_address = "192.168.1.129"

    client = ApiClient(tapo_username, tapo_password)
    device = await client.p110(ip_address)

    device_info = await device.get_device_info()
    print(f"Device info: {device_info.to_dict()}")

    device_usage = await device.get_device_usage()
    print(f"Device usage: {device_usage.to_dict()}")

    current_power = await device.get_current_power()
    print(f"Current power: {current_power.to_dict()}")

    energy_usage = await device.get_energy_usage()
    print(f"Energy usage: {energy_usage.to_dict()}")

    today = datetime.today()
    energy_data_hourly = await device.get_energy_data(EnergyDataInterval.Hourly, today)
    print(f"Energy data (hourly): {energy_data_hourly.to_dict()}")

    energy_data_daily = await device.get_energy_data(
        EnergyDataInterval.Daily,
        datetime(today.year, get_quarter_start_month(today), 1),
    )
    print(f"Energy data (daily): {energy_data_daily.to_dict()}")

    energy_data_monthly = await device.get_energy_data(
        EnergyDataInterval.Monthly,
        datetime(today.year, 1, 1),
    )
    print(f"Energy data (monthly): {energy_data_monthly.to_dict()}")


def get_quarter_start_month(today: datetime) -> int:
    return 3 * ((today.month - 1) // 3) + 1


if __name__ == "__main__":
    asyncio.run(main())