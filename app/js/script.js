$(document).ready(function () {
    $('.js-example-basic-single').select2();
});

var url = window.location.origin.substr(0, window.location.origin.indexOf(":") + 1) + "//" + "modelservice." + window.location.origin.substr(window.location.origin.indexOf(".") + 1) + '/model'

console.log(var url);

function go_fetch() {
    var post_data = {
        request: {
            feature: d3.select('#latitude').property("value") + "," +
                d3.select('#longitude').property("value") + "," +
                d3.select('#pressure').property("value") + "," +
                d3.select('#avgpressure').property("value") + "," +
                d3.select('#airtemperature').property("value") + "," +
                d3.select('#dewpoint').property("value") + "," +
                d3.select('#humidity').property("value") + "," +
                d3.select('#winddirection').property("value") + "," +
                d3.select('#avgwindspeed').property("value") + "," +
                d3.select('#windspeedchange').property("value")
     
        }
    };

    fetch(url, {
        method: 'POST', // or 'PUT'
        body: JSON.stringify(post_data), // data can be `string` or {object}!
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(response => response.json())
        .then(data => d3.select("#pred_value").text("Predicted Value: " + (data.response.prediction.prediction == 0 ? "Not Canceled" : "Canceled")) &
            d3.select("#proba_value").text("Probability: " + (data.response.prediction.proba)))
        .catch(error => console.error('Error:', error));
}
