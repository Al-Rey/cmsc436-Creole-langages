from flask import Flask, render_template,request
from read_data import *

app = Flask(__name__)

#User word/phrase input
@app.route('/', methods=['GET'])
def input():
    return render_template("input.html")

#Page of data analysis on language data
@app.route('/images')
def images():
    return render_template("images.html")


# Interactive map
@app.route('/index', methods = ['POST', 'GET'])
def root():

    #Getting user input to query database
    english_word = request.form.get('English')
    creole_word = request.form.get('Creole')

    #Checks which selection box was used and creates the corresponsing markers
    if creole_word != None:
        word = creole_word
        markers = creole_markers(word)
    else:
        word = english_word
        markers = english_markers(word)


    return render_template("index.html",markers=markers)