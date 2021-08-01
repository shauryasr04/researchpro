from flask import Flask, url_for, render_template, app, redirect
import os
import jinja2
from markupsafe import escape
from flask import request
import requests
from requests import get
from bs4 import BeautifulSoup
import spacy
from spacy import displacy
import en_core_web_lg
import pandas as pd
import urllib.request, urllib.error, urllib.parse

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader (template_dir))


def printTohtml(Alist,required_univ):
    import time    
    html =  "<html>\n<head></head>\n<style> body { background-color: HoneyDew;} h1 { text-align:center; color: black;} p { margin: 0 !important; text-align:center; color: white;}</style>"
    title = "Your Results!"
    html = html+ '<h1>' + title + '</h1>'
    #html = html + '<iframe src="https://www.nfl.com/" title="NFL HERE">'

    for line in Alist:
        likedprofname = ""
        website = get_prof_link(line, required_univ)
        if(website != ""):
            time.sleep(1)   
            para = '<p>' + "<a href =" + website + ">" + line +  "</a>" +'"        " <button type = "button" onclick= alert("Added to Liked List") > Like </button> </p>'
            html = html+ para 
    # with open(htmlfile, 'w') as f:
        #  f.write(html + "</body>\n</html>")
    return html

def get_prof_link (name, univ):
    subscription_key = "5b1d8775f8fd485e9fd2bea8c1d21d16"
    search_url = "https://api.bing.microsoft.com/v7.0/search"
    search_term = name +' '+ "site:" + univ+".edu"
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {"q": search_term, "textDecorations": True, "textFormat": "HTML","count": 1}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    try:
        for searchresult in search_results["webPages"]["value"]:
            url = searchresult["url"]
            print(name)
            print(url)
    except:
        url=""
        print("error")
    return url

jinja_env.globals.update(printTohtml=printTohtml)





