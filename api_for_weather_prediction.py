import time
import json
import uvicorn
import pandas as pd
from pydantic import BaseModel
from http.client import REQUEST_TIMEOUT
from prophet.serialize import  model_from_json
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


with open('weather_forecast_model.json', 'r') as fin:
    weather_forecast_model = model_from_json(fin.read())  # Load model

@app.post("/get-weather-prediction")
def evaluate(date: str = Form()):
    # print("here")
    t1 = time.time()
    future_dates = pd.DataFrame(columns=['ds'])
    future_dates.loc[0] = [date]


    forecast = weather_forecast_model.predict(future_dates)
    lowest_temp = forecast['yhat_lower'][0]
    highest_temp = forecast['yhat_upper'][0]
    temp = forecast['yhat'][0]
    return {
        "highest_temperature": highest_temp,
        "actual_temperature": temp,
        "lowest_temperature": lowest_temp
    }


if __name__ == "__main__":
    uvicorn.run("api_for_weather_prediction:app", host='0.0.0.0', port=5009, reload=False)