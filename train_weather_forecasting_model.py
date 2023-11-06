import numpy as np
import pandas as pd
from prophet import Prophet
from prophet.serialize import model_to_json

if __name__ == "__main__":
    past_temperature_data = pd.read_csv("./data_2015_to_2023.csv")
    past_temperature_data = past_temperature_data.rename(columns={'time': 'ds',
                        'temperature_2m': 'y'})

    weather_forecast_model = Prophet(interval_width=0.95)
    weather_forecast_model.fit(past_temperature_data)

    ## saving the model as a serialized json file 
    with open('weather_forecast_model.json', 'w') as fout:
        fout.write(model_to_json(weather_forecast_model)) 