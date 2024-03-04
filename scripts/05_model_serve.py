"""
In this code the generation of an endpoint for the model prediction takes place.
"""

#Example:
#args = { "feature": "0.0000,0.0000,100,950,0.0,0.0,0.0,0.0,0.0,0.0" } 

import os

#Detecting the operating system full path:
full_path = os.getenv("OPERATING_SYSTEM_PATH")
     
if full_path is None: 
   #Element doesn't exist.
   os.environ["OPERATING_SYSTEM_PATH"] = "/home/cdsw/"

#Detecting the prediction object model option.
use_prebuilt_model = os.getenv("USE_PREBUILT_MODEL")

if full_path is None: 
   #Element doesn't exist.
   os.environ["USE_PREBUILT_MODEL"] = "yes"

import cdsw
import json
import pickle
import numpy as np
import pandas as pd

model = None 
pipeline = None 

#Reading both model and pipeline objects. Unless we are told otherwise, we take the 
#path with the prebuilt elements. 

if os.getenv("USE_PREBUILT_MODEL") == "yes" or os.getenv("USE_PREBUILT_MODEL") is None: 
    #This doesn't start with slash
    with open(os.getenv("OPERATING_SYSTEM_PATH") + "src/prebuilt-models/ensemble_model3.pkl",'rb') as f:
         model = pickle.load(f)
else: 
    with open(os.getenv(os.getenv("OPERATING_SYSTEM_PATH") + "src/models/ensemble_model3.pkl",'rb') as f:
         model = pickle.load(f) 


if os.getenv("USE_PREBUILT_MODEL") == "yes" or os.getenv("USE_PREBUILT_MODEL") is None: 
    #This doesn't start with slash
    with open(os.getenv("OPERATING_SYSTEM_PATH") + "src/prebuilt-models/pipeline.pkl",'rb') as f:
         pipeline = pickle.load(f)

else: 
    with open(os.getenv("OPERATING_SYSTEM_PATH") + "src/models/pipeline.pkl",'rb') as f:
         pipeline = pickle.load(f)


@cdsw.model_metrics
def predict_wind_speed(args):
    inputs = args["feature"].split(",")

    latitude = float(inputs[0])
    longitude = float(inputs[1])
    pressure = float(inputs[2])
    avg_pressure = float(inputs[3])
    air_temperature = float(inputs[4])
    dew_point = float(inputs[5])
    humidity = float(inputs[6])
    wind_direction = float(inputs[7])
    avg_windspeed = float(inputs[8])
    wind_speed_ratio = float(inputs[9])

    input_variables = [[latitude, longitude, pressure, air_temperature, dew_point, humidity, 0, 0, wind_direction, avg_pressure, avg_windspeed, wind_speed_ratio]]

    transformed_variables = pipeline.transform(input_variables)

    prediction = model.predict(transformed_variables)[0]
     
    cdsw.track_metric("input_data", args)
    cdsw.track_metric("prediction", float(prediction))

    response = {
                 "original_input": {
                                    'Latitude': latitude,
                                    'Longitude': longitude,
                                    'Pressure': pressure, 
                                    'Average Pressure': avg_pressure,
                                    'Air Temperature': air_temperature,
                                    'Dew Point': dew_point,
                                    'Relative Humidity': humidity,
                                    'Wind Direction': wind_direction,
                                    'Average Wind Speed':avg_windspeed,
                                    'Wind Speed Change Ratio':wind_speed_ratio
                                   },
         
         
                 "result": float(prediction),
                 "latitude_x": latitude,
                 "longitude_y": longitude
               }
     
    return response
