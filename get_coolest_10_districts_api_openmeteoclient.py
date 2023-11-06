import json
import time
import pandas as pd
import openmeteo_requests
from openmeteo_sdk.Variable import Variable

url = "https://api.open-meteo.com/v1/forecast"
om = openmeteo_requests.Client()


with open('./lat_long_info.json', 'r') as file:
    dictrict_lat_long_data = json.load(file)


if __name__ == "__main__":
    t1 = time.time()
    info = dictrict_lat_long_data['districts']
    average_temp_all_districts = []
    
    for district in info:
        temp_sum = 0
        name = district['bn_name']
        lat = district['lat']
        long = district['long']

        params = {
                "latitude": lat,
                "longitude": long,
                "hourly": ["temperature_2m"]
            }
        responses = om.weather_api(url, params=params)
        response = responses[0]
        hourly = response.Hourly()

        hourly_variables = list(map(lambda i: hourly.Variables(i), range(0, hourly.VariablesLength())))
        hourly_temperature_2m = next(filter(lambda x: x.Variable() == Variable.temperature and x.Altitude() == 2, hourly_variables)).ValuesAsNumpy()

        temp_sum += hourly_temperature_2m[14]
        for i in range(38,len(hourly_temperature_2m), 24):
            temp_sum += hourly_temperature_2m[i]
        average_temp_all_districts.append(temp_sum/7)
    
