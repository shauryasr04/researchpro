# application.py
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1>Hello World! Shaurya \n How are you all doing?</h1>"