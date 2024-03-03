$(document).ready(function () {
    $('.js-example-basic-single').select2();
});

var url = window.location.origin.substr(0, window.location.origin.indexOf(":") + 1) + "//" + "modelservice." + window.location.origin.substr(window.location.origin.indexOf(".") + 1) + '/model'

   <form action="{{ url_for('main') }}" method="POST" onsubmit="return actualizarMapa()">
      <p><label><i class="fa fa-globe"></i> Latitude</label></p>
      <input class="w3-input w3-border" type="number" value="0.0000" id="latitude" name="latitude" min="-90" max="90" step="0.0001" required>      
      <p><label><i class="fa fa-globe"></i> Longitude</label></p>
      <input class="w3-input w3-border" type="number" value="0.0000" id="longitude" name="longitude" min="-180" max="180" step="0.0001" required>       
      <p><label><i class="fa fa-area-chart"></i> Pressure</label></p>
      <input type="range" value="100" name="pressure" min="100" max="1050" step="1" oninput="this.nextElementSibling.value = this.value" required><output>100</output>
      <p><label><i class="fa fa-tachometer"></i> Average Pressure (hPa)</label></p>
      <input type="range" value="0.0" name="avgpressure" min="950" max="1050" step="1" oninput="this.nextElementSibling.value = this.value" required><output>0</output>        
      <p><label><i class="fa fa-thermometer-full"></i> Air Temperature (ºC)</label></p>
      <input type="range" value="0.0" name="airtemperature" min="-50" max="60" step="0.05" oninput="this.nextElementSibling.value = this.value" required><output>0</output>
      <p><label><i class="fa fa-thermometer-full"></i> Dew Point (ºC)</label></p>
      <input type="range" value="0.0" name="dewpoint" min="-30" max="30" step="0.05" oninput="this.nextElementSibling.value = this.value" required><output>0</output>
      <p><label><i class="fa fa-tint"></i> Relative Humidity in percentage (%)</label></p>
      <input type="range" value="0.0" name="humidity" min="0" max="100" step="1" oninput="this.nextElementSibling.value = this.value" required><output>0</output>
      <p><label><i class="fa fa-arrow-circle-o-right"></i> Wind Direction (º)</label></p>
      <input type="range" value="0.0" name="winddirection" min="0" max="359" step="1" oninput="this.nextElementSibling.value = this.value" required><output>0</output>
      <p><label><i class="fa fa-arrow-circle-o-right"></i> Average Wind Speed (kt)</label></p>
      <input type="range" value="0.0" name="avgwindspeed" min="0" max="100" step="1" oninput="this.nextElementSibling.value = this.value" required><output>0</output>
      <p><label><i class="fa fa-percent"></i> Wind Speed Change Ratio </label></p>
      <input type="range" value="0.0" name="windspeedchange" min="0" max="100" step="0.1" oninput="this.nextElementSibling.value = this.value" required><output>0</output> 
      <p><button class="w3-button w3-block w3-green w3-center-align" type="submit"><i class="fa fa-search w3-margin-right"></i> Calculate</button></p>
    </form>

function go_fetch() {
    var post_data = {
        request: {
            feature: d3.select('#').property("value") + "," +
                d3.select('#').property("value") + "," +
                d3.select('#').property("value") + "," +
                d3.select('#').property("value") + "," +
                d3.select('#').property("value") + "," +
                d3.select('#').property("value") + "," +
                d3.select('#').property("value") + "," +
                d3.select('#').property("value") + "," +
                d3.select('#').property("value") + "," +
                d3.select('#').property("value") + "," +
                d3.select('#').property("value") + "," +
                d3.select('#').property("value")

            
        }
    };

    fetch(url, {
        method: 'POST', // or 'PUT'
        body: JSON.stringify(post_data), // data can be `string` or {object}!
        headers: {
            'Content-Type': 'application/json',
            //'Authorization' : 'Bearer ' + model_api_key
        }
    })
        .then(response => response.json())
        .then(data => d3.select("#pred_value").text("Predicted Value: " + (data.response.prediction.prediction == 0 ? "Not Canceled" : "Canceled")) &
            d3.select("#proba_value").text("Probability: " + (data.response.prediction.proba)))
        .catch(error => console.error('Error:', error));
}
