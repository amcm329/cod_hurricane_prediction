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

#ct = load("/home/cdsw/src/prebuilt-models/ct.joblib")
#pipe = load("/home/cdsw/src/prebuilt-models/pipe.joblib")

"""
ct = load("src/prebuilt-models/ct.joblib")
pipe = load("src/prebuilt-models/pipe.joblib")
"""

full_path =  os.getenv("SPARK_CONNECTION_NAME")

model = None 

#This doesn't start with slash
with open("src/prebuilt-models/best_model_tuned.pkl",'rb') as f:
     model = pickle.load(f)


#args = {"feature": "-50,50,100"}

@cdsw.model_metrics
def predict_cancelled(args):
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
