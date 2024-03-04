import os
import flask
import pickle
import requests
from joblib import load

#This doesn't start with slash
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

        #In case the call fails, we predict with local objects. 
        try:
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
    #app.run()
    app.run(host="127.0.0.1", port=int(os.environ["CDSW_READONLY_PORT"]))
