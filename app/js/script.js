$(document).ready(function () {
    $('.js-example-basic-single').select2();
});

var url = window.location.origin.substr(0, window.location.origin.indexOf(":") + 1) + "//" + "modelservice." + window.location.origin.substr(window.location.origin.indexOf(".") + 1) + '/model'

function go_fetch() {
    var post_data = {
        request: {
            feature: d3.select('#carrier').property("value") + "," +
                d3.select('#origin').property("value") + "," +
                d3.select('#destination').property("value") + "," +
                d3.select('#week').property("value") + "," +
                d3.select('#departure').property("value")
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
