# application.py
from flask import Flask, url_for
from markupsafe import escape
from flask import request
from envs.pythonProject3.Lib.http import cookies

app = Flask(__name__)
@app.route('/')
def hello():
    return '<h1> Hello World! How are you doing! </h>'
def index():
    username = cookies.request.get('username')