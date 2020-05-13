import json
from os import environ

from flask import Flask, request
from requests import get

DEVELOPMENT = environ["FLASK_ENV"] == "development"
WEBPACK_DEV_SERVER = "http://localhost:3000"

app = Flask(__name__, static_folder=None if DEVELOPMENT else "static")


def proxy(path):
    response = get(f"{WEBPACK_DEV_SERVER}{path}")
    excluded_headers = [
        "content-encoding",
        "content-length",
        "transfer-encoding",
        "connection",
    ]
    headers = {
        name: value
        for name, value in response.raw.headers.items()
        if name.lower() not in excluded_headers
    }
    return (response.content, response.status_code, headers)


@app.route("/api/hello")
def apiHello():
    return json.dumps("Andrew")


@app.route("/app/", defaults={"path": "index.html"})
@app.route("/app/<path:path>", methods=["GET"])
def getApp(path):
    if DEVELOPMENT:
        return proxy(request.path)
    return app.send_static_file(path)
