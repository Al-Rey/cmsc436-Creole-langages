from flask import Flask, render_template,request
import json
import csv

app = Flask(__name__)

##  Global variables to define creole dictionary location and coordinates
##
CREOLE_LOCATIONS = {"haitian": [-72.285,18.9712], "jamaican": [-77.2975,18.1096], "cayman": [-81.2546,19.3133]}
CREOLE_DICTIONARY_LIST = {"haitian":"scraping_scripts/hatian_creole_dictionary_v3.csv"}
CREOLE_LIST = ["haitian"]

#Reading database to find if word appears in creole
def read_database(word,creole):
    with open(CREOLE_DICTIONARY_LIST[creole],'r',newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['word'] == word:
                return (row['creole_word'])
    return("WORD_NOT_FOUND")

#User word/phrase input
@app.route('/')
def input():
    return render_template("input.html")

# Interactive map
@app.route('/index', methods = ['POST', 'GET'])
def root():

    #Getting user input to query database
    word = request.form["Word/Phrase"]
    creole_word = {}
    for creole in CREOLE_LIST:
        creole_word[creole] = read_database(word,creole)

    #Creating Python Dictionary in form of geojson to be converted to json later
    creole_dict = {"type":"FeatureCollection","features":[]}
    for creole in creole_word:
        creole_dict["features"].append(
            {
            "type":"Feature",
            "properties":{"creole_language": creole, "word": word, "creole_word":creole_word[creole]},
            "geometry":{"coordinates":CREOLE_LOCATIONS[creole],"type":"Point"}
            })

    #Converting Python Dictionary to Json
    creole_json = json.dumps(creole_dict)

    #Saving Json to locations.json to be read by index.html
    with open("locations.json", "w") as outfile:
        outfile.write(creole_json)
    f = open("locations.json")
    markers = json.load(f)

    return render_template("index.html",markers=markers)