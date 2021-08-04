# application.py
from typing import Dict
from flask import Flask, url_for, render_template, app 
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
import numpy as np

app = Flask(__name__)
class ProfInfo:
    def __init__(self, name , link):
        self.name = name
        self.link = link

def unique(list1):
    x = np.array(list1)
    return (np.unique(x))

def Python_execute (one,two):
    subscription_key = "5b1d8775f8fd485e9fd2bea8c1d21d16"
    assert subscription_key
    search_url = "https://api.bing.microsoft.com/v7.0/search"
    required_field = str(one)
    required_univ = str(two)
    search_term = required_field + " faculty site:" + required_univ + ".edu"
    #search_term = "fintech faculty site:duke.edu"
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {"q": search_term, "textDecorations": True, "textFormat": "HTML", "count":2}
    response = requests.get(search_url, headers=headers, params=params) 
    response.raise_for_status()
    search_results = response.json()
    nlp = spacy.load('en_core_web_lg')
    counter =0
    listofNames =[]
    listofNamesBN = []
    for searchresult in search_results["webPages"]["value"]:
        url = searchresult["url"]
        print(url)
        try:   
            response = get(url).content
            soup = BeautifulSoup(response)
            for script in soup(["script", "style"]):
                script.extract()
            counter = counter+1
            f= open(str(counter)+".txt","w",encoding='utf-8')
            #print(counter)
            cleanedtext = soup.text.strip('\t\r\n')
            f.write(cleanedtext)
            f.close()
            doc = nlp(cleanedtext)
            for ent in doc.ents:
                if(ent.label_ == 'PERSON'):
                    print(ent.text)
                    listofNames.append(ent.text)
        except:
            print("ERROR HAPPENED")
        for i in range(len(listofNames)):
            doc2 = nlp(listofNames[i])
            for ent in doc2.ents:
                if(ent.label_== 'PERSON'):
                    listofNamesBN.append(ent.text)
    listofNames_edited = listofNamesBN[:10]
    listofNames_FINAL = unique(listofNames_edited)
    return listofNames_FINAL

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

def GetProfData(Alist, required_univ):
    profInfoArray =[]
    for line in Alist:
        website = get_prof_link(line, required_univ)
        profInfo = ProfInfo(line,website)
        profInfoArray.append(profInfo)
    return profInfoArray
              
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
@app.route('/')
def home():
    return render_template("templatetrial.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/action_page')
def action():
    input_one = request.args["ffield"] 
    input_two = request.args["funiv"]
    input_three = Python_execute(input_one, input_two)
    profInfoArray= GetProfData(input_three,input_two)
    return render_template('TTcopy.html', profInfoList = profInfoArray)

if __name__ == "__main__":
    app.run(debug=True)
    