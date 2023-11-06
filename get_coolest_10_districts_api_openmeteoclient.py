import json
import time
import uvicorn
import schedule
import pandas as pd
import openmeteo_requests
from itertools import islice
from pydantic import BaseModel
from http.client import REQUEST_TIMEOUT
from openmeteo_sdk.Variable import Variable
from fastapi import FastAPI, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

url = "https://api.open-meteo.com/v1/forecast"
om = openmeteo_requests.Client()


with open('./lat_long_info.json', 'r') as file:
    dictrict_lat_long_data = json.load(file)

def generate_top_ten_coldest_district():
    t1 = time.time()
    info = dictrict_lat_long_data['districts']
    districts_average_temp = {}
    
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
 
        districts_average_temp[name] = temp_sum/7

    with open("./top_10_coldest_district_for_today.json", 'w') as file:
        json.dump(districts_average_temp, file)

schedule.every().day.at("00:00").do(generate_top_ten_coldest_district) ## generate top 10 coldest district json at 12:00 AM everyday

@app.get("/top-10-coldest-districts")
def evaluate():
    with open('./top_10_coldest_district_for_today.json', 'r') as file:
        data = json.load(file)
    
    sorted_districts_average_temp_dict = dict(sorted(data.items(), key=lambda item: item[1]))
    ten_coldest_districts = dict(islice(sorted_districts_average_temp_dict.items(), 10))

    return ten_coldest_districts

if __name__ == "__main__":
    # generate_top_ten_coldest_district()
    uvicorn.run("get_coolest_10_districts_api_openmeteoclient:app", host='0.0.0.0', port=5010, reload=False)
