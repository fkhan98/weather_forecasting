import pandas as pd
from prophet.serialize import  model_from_json


with open('weather_forecast_model.json', 'r') as fin:
    weather_forecast_model = model_from_json(fin.read())  # Load model

if __name__ == "__main__":
    # future_dates = weather_forecast_model.make_future_dataframe(periods=36, freq='MS')
    # print(future_dates.head())
    future_dates = pd.DataFrame(columns=['ds'])
    future_dates.loc[0] = ['2023-12-30 14:00:00']


    forecast = weather_forecast_model.predict(future_dates)
    lowest_temp = forecast['yhat_lower']
    highest_temp = forecast['yhat_upper']
    temp = forecast['yhat']
    print(lowest_temp, highest_temp, temp)
    # print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].head())