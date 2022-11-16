from flask import Flask, render_template,request
from read_data import *

app = Flask(__name__)

#User word/phrase input
@app.route('/', methods=['GET'])
def input():
    return render_template("input.html")


# Interactive map
@app.route('/index', methods = ['POST', 'GET'])
def root():

    isCreole = False
    #Getting user input to query database
    english_word = request.form.get('English')
    creole_word = request.form.get('Creole')

    word = ""
    if english_word != None:
        word = english_word
        markers = english_markers(word)
    else:
        word = creole_word
        markers = english_markers(word)
        isCreole = True


    return render_template("index.html",markers=markers,isCreole=isCreole)