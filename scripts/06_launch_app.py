
import os
import random
import logging
from pandas.io.json import dumps as jsonify
from IPython.display import Javascript, HTML
from flask import Flask, send_from_directory, request

# This enables an interactive debugger.
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

app = Flask(__name__, static_url_path="")

@app.route("/")
def home():
    return "<script> window.location.href = '/app/index.html'</script>"


@app.route("/app/<path:path>")
def send_file(path):
    return send_from_directory("app", path)

HTML(
    "<a href='https://{}.{}'>Open Table View</a>".format(
        os.environ["CDSW_ENGINE_ID"], os.environ["CDSW_DOMAIN"]
    )
)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ["CDSW_READONLY_PORT"]))
