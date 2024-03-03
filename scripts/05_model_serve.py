"""
In this code the generation of an endpoint for the model prediction takes place.
"""

import numpy as np
import pandas as pd
import cdsw
#import cml.metrics_v1 as metrics
#import cml.models_v1 as models
import json
from joblib import dump, load
import pickle

# args = {"feature" : "US,DCA,BOS,1,16"}
#Homedir is /home/cdsw

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


ct = None
pipe = None 
model = None 

#Reading both model and pipeline objects. Unless we are told otherwise, we take the 
#path with the prebuilt elements. 

if os.getenv("USE_PREBUILT_MODEL") == "yes": 
    model = load(os.getenv("OPERATING_SYSTEM_PATH") + "src/prebuilt-models/ct.joblib")

else: 
    model = load(os.getenv("OPERATING_SYSTEM_PATH") + "src/models/ct.joblib")

if os.getenv("USE_PREBUILT_MODEL") == "yes": 
    pipeline = load(os.getenv("OPERATING_SYSTEM_PATH") + "src/prebuilt-models/pipe.joblib")

else: 
    pipeline = load(os.getenv("OPERATING_SYSTEM_PATH") + "src/models/pipe.joblib")


#This doesn't start with slash
#with open(os.getenv("OPERATING_SYSTEM_PATH") + "src/prebuilt-models/best_model_tuned.pkl",'rb') as f:
#     model = pickle.load(f)

#args = {"feature": "-50,50,100"}

#--------------------------------------------------------------------------------------------------------

        latitude = flask.request.form['latitude']
        longitude = flask.request.form['longitude']
        pressure = flask.request.form['pressure']
        avg_pressure = flask.request.form['avgpressure']
        air_temperature = flask.request.form['airtemperature']
        dew_point = flask.request.form['dewpoint']
        humidity = flask.request.form['humidity']
        wind_direction = flask.request.form['winddirection']
        avg_windspeed = flask.request.form['avgwindspeed']
        wind_speed_ratio = flask.request.form['windspeedchange']

        input_variables = [[latitude, longitude, pressure, air_temperature, dew_point,
                            humidity, 0, 0, wind_direction, avg_pressure, avg_windspeed, wind_speed_ratio,
                            ]]

        transformed_variables = pipeline.transform(input_variables)

        prediction = model.predict(transformed_variables)[0]

        return flask.render_template('index.html',
                                     original_input = {'Latitude':latitude,'Longitude':longitude,'Pressure':pressure, 
                                                      'Average Pressure':avg_pressure,'Air Temperature':air_temperature,
                                                      'Dew Point':dew_point,'Relative Humidity':humidity,'Wind Direction':wind_direction,
                                                      'Average Wind Speed':avg_windspeed,'Wind Speed Change Ratio':wind_speed_ratio},
                                     result = prediction,
                                     latitude_x = latitude,
                                     longitude_y = longitude)

#---------------------------------------------------------------------------------------------------------

@cdsw.model_metrics
def predict_wind_speed(args):
    inputs = args["feature"].split(",")

    latitude = float(inputs[0])
    longitude = float(inputs[1])
    pressure = float(inputs[2])
    
    input_variables = [[latitude, longitude, pressure]]
    
    # Falta scaler ojo!
    prediction = model.predict(input_variables)[0]

    cdsw.track_metric("input_data", args)
    cdsw.track_metric("prediction", int(prediction))
    
    response = {"prediction": int(prediction)}

    return response







"""
@cdsw.model_metrics
def predict_cancelled(args):
    inputs = args["feature"].split(",")
    inputs[3] = int(inputs[3])
    inputs[4] = int(inputs[4])


    input_cols = [
        "uniquecarrier",
        "origin",
        "dest",
        "week",
        "hour",
    ]
    input_df = pd.DataFrame([inputs], columns=input_cols)

    input_transformed = ct.transform(input_df)

    probas = pipe.predict_proba(input_transformed)
    prediction = np.argmax(probas)
    proba = round(probas[0][prediction], 2)
    
    cdsw.track_metric("input_data", args)
    cdsw.track_metric("prediction", int(prediction))
    cdsw.track_metric("proba", str(proba))
    
    response = {"prediction": int(prediction), "proba": str(proba)}

    return response
    """
