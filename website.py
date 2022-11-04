from flask import Flask, render_template,request
import os
import json

app = Flask(__name__)

#User word/phrase input
@app.route('/')
def input():
    return render_template("input.html")


# Interactive map
@app.route('/index', methods = ['POST', 'GET'])
def root():

    #Getting user input to query database
    word = request.form

    f = open("locations.json")
    markers = json.load(f)

    """location_data =[   
        {'lat':19.3133,'lon':-81.2546,'tooltip':'Cayman Islands English Cayman Creole'},
        {'lat':18.7357,'lon':-70.1627,'tooltip':'Dominican Republic Spanish Haitian Creole'},
        {'lat':18.9712	,'lon':-72.2852,'tooltip':'Haiti French Haitian Creole'},
        {'lat':18.1096,'lon':-77.2975,'tooltip':'Jamaica English Jamaican Patois'},
        {'lat':18.2208,'lon':-66.5901,'tooltip':'Puert Rico (Haitian Creole Minority Population)'},
        {'lat':21.5218,'lon':-77.7812,'tooltip':'Cuba (Haitian Creole Minority Population)'}
    ]"""

    return render_template("index.html",markers=markers,word=word)