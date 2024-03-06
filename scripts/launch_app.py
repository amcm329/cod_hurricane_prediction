"""
  This code launches a Flask server to enable the app and also handle model requests.
"""

import os
import flask
import pickle
import requests
from joblib import load

#Checking path environment variable.
full_path = os.getenv("OPERATING_SYSTEM_PATH")
     
if full_path is None: 
   #Element doesn't exist.
   os.environ["OPERATING_SYSTEM_PATH"] = "/home/cdsw/"

#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------

"""
   IMPORTANT: these values are relevant to call the model endpoint, that is why it's recommended that 
   both the model deployment and the application initialization be enabled in separate steps.
"""
model_endpoint = None # Example: 'http://modelservice.cdsw.44.232.253.206.nip.io/model'
model_access_key = None # Example: "m03jfhnxm1ea6hhdoia94qa3p0kceuse"

#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------

#As a security measure, we load the prebuilt model in case the model endpoint fails.
model = load(os.getenv("OPERATING_SYSTEM_PATH") + "src/prebuilt-models/ensemble_model3.pkl")
pipeline = load(os.getenv("OPERATING_SYSTEM_PATH") + "src/prebuilt-models/pipeline.pkl")

#Changed to app folder
#By default template_folder is "template"
app = flask.Flask(__name__, template_folder='app')

#Check path
#This starts with slash
@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        return(flask.render_template('index.html'))
    if flask.request.method == 'POST':
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

        prediction = None 
        transformed_variables = pipeline.transform(input_variables)

        #In case the model API call fails, we predict with local objects. 
        #We couldn't find a way of automatically call a model endpoint since apparently theres no chance of
        #retrieving the access key BEFORE the deployment, or there isn't a free way of getting access either.
        
        #https://docs.cloudera.com/machine-learning/cloud/models/topics/ml-model-access-key.html          
        try:
             if model_enpoint is not None and model_access_key is not None:
                #Example
                #r = requests.post(model_endpoint,timeout=70, data="{'accessKey':{0}, 'request':{'feature':\"0.0000,0.0000,100,950,0.0,0.0,0.0,0.0,0.0,0.0\")}, headers={'Content-Type': 'application/json'}}, timeout=70").format(model_access_key,string_data))
                string_data = "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}".format(latitude,longitude,pressure,avg_pressure,air_temperature,dew_point,humidity,wind_direction,avg_windspeed,wind_speed_ratio)
                #r = requests.post(model_endpoint,timeout=70, data="{'accessKey':{0}, 'request':{'feature':\"{1}\")}, headers={'Content-Type': 'application/json'}}, timeout=70").format(model_access_key,string_data))

                prediction = model.predict(transformed_variables)[0]
               
                #prediction = r["result"]
                print("API call")
                  
             else:
                prediction = model.predict(transformed_variables)[0]
           
        except:     
           prediction = model.predict(transformed_variables)[0]
  
        return flask.render_template('index.html',
                                     original_input = {'Latitude':latitude,'Longitude':longitude,'Pressure':pressure, 
                                                      'Average Pressure':avg_pressure,'Air Temperature':air_temperature,
                                                      'Dew Point':dew_point,'Relative Humidity':humidity,'Wind Direction':wind_direction,
                                                      'Average Wind Speed':avg_windspeed,'Wind Speed Change Ratio':wind_speed_ratio},
                                     result = prediction,
                                     latitude_x = latitude,
                                     longitude_y = longitude)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=int(os.environ["CDSW_READONLY_PORT"]))
