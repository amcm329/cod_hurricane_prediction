
import flask
import pickle

# Use pickle to load in the pre-trained model.

with open(f'src/prebuilt-models/best_model_tuned.pkl','rb') as f:
    model = pickle.load(f)

app = flask.Flask(__name__, template_folder='web_page')

@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        return(flask.render_template('index.html'))
    if flask.request.method == 'POST':
        latitude = flask.request.form['latitude']
        longitude = flask.request.form['longitude']
        pressure = flask.request.form['pressure']

        input_variables = [[latitude, longitude, pressure]]
        # Falta scaler ojo!
        prediction = model.predict(input_variables)[0]
        return flask.render_template('index.html',
                                     original_input = {'Latitude':latitude,'Longitude':longitude,'Pressure':pressure},
                                     result=prediction)
if __name__ == '__main__':
    app.run()
