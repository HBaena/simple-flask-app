from flask import Flask  # Core of flask apps
from flask_restful import Api  # modules for fast creation of apis
from os import path, getcwd


app = Flask(__name__)  # Creating flask app
app.secret_key = ''  # Declaring secret api

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["DEBUG"] = False

api = Api(app)  # Creating API object from flask app
