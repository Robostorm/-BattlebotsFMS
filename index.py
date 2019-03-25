from flask import flask
import gpiozero

FMS = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
