import numpy as np
import pandas as pd

import cdsw
#import cml.metrics_v1 as metrics
#import cml.models_v1 as models

import json
from joblib import dump, load

# args = {"feature" : "US,DCA,BOS,1,16"}

ct = load("/home/cdsw/src/prebuilt-models/ct.joblib")
pipe = load("/home/cdsw/src/prebuilt-models/pipe.joblib")


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
