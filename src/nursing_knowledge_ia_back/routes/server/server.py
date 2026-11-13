from flask import Flask
from flask_cors import CORS

def StartServer():
    app = Flask(__name__)
    CORS(app)


    return app
