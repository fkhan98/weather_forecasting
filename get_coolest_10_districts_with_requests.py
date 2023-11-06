import json
import time
import requests
import pandas as pd
import openmeteo_requests
from openmeteo_sdk.Variable import Variable



with open('./lat_long_info.json', 'r') as file:
    dictrict_lat_long_data = json.load(file)


if __name__ == "__main__":
    t1 = time.time()
    info = dictrict_lat_long_data['districts']
    average_temp_all_districts = []
    
    for district in info:
        temp_sum = 0
        name = district['bn_name']
        latitude = district['lat']
        longitude = district['long']

        result_weather = requests.get(url='https://api.open-meteo.com/v1/forecast?latitude=' + latitude + '&longitude=' + longitude + '&hourly=temperature_2m&forecast_days=7')
        data = result_weather.json()
        hourly_temperature = data['hourly']['temperature_2m']
        # print(len(hourly_temperature))
        temp_sum += hourly_temperature[14]
        for i in range(38,len(hourly_temperature), 24):
            temp_sum += hourly_temperature[i]
        average_temp_all_districts.append(temp_sum/7)

    t2 = time.time()
    print(average_temp_all_districts)
    print(t2-t1)