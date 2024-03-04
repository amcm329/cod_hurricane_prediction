import os
import flask
import pickle
import joblib

#This doesn't start with slash
with open(f'/home/cdsw/src/prebuilt-models/ensemble_model3.pkl','rb') as f:
    model = joblib.load(f)

with open(f'/home/cdsw/src/prebuilt-models/pipeline.pkl','rb') as f:
    pipeline = joblib.load(f)

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

        transformed_variables = pipeline.transform(input_variables)
        prediction = model.predict(transformed_variables)[0]

        #Poner aqui lo de la llamada.  
        
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
