# application.py
from flask import Flask, url_for , request

app = Flask(__name__)
@app.route('/')
def hello():
    return '<h1> HI Radhika! You are cute </h1>'

@app.route('/radzclown')
def radzclown():
    return '<h1> Hi radhika, you are a clown </h1>'