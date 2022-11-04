from flask import Flask, render_template,request
import os
import json

##
## https://medium.com/geekculture/how-to-make-a-web-map-with-pythons-flask-and-leaflet-9318c73c67c3
## https://www.askpython.com/python-modules/flask/flask-forms
##
##


def read_database(phrase):
    return 0

app = Flask(__name__)

# Interactive map
#   1. Display blank map of the Caribbean -- probably will use openstreetmaps
#   2. Color different countries different colors
#   3. Allow user selection 
#       3a. Alpha -- select Creole language and display it's location on map 
@app.route('/')
def input():
    return render_template("input.html")

@app.route('/index', methods = ['POST', 'GET'])
def root():

    ## QUERY DATABASE WITH WORD HERE
    #location_data = read_database(word)

    #word = request.form

    #HEX COLORS
    #RED - #FF0000
    #BLUE - #0000FF
    #GREEN - #00FF00
    #YELLOW - #FFFF00

    f = open("locations.geojson")
    location_data = json.load(f)

    print(location_data)

    """location_data =[   
        {'lat':19.3133,'lon':-81.2546,'tooltip':'Cayman Islands English Cayman Creole'},
        {'lat':18.7357,'lon':-70.1627,'tooltip':'Dominican Republic Spanish Haitian Creole'},
        {'lat':18.9712	,'lon':-72.2852,'tooltip':'Haiti French Haitian Creole'},
        {'lat':18.1096,'lon':-77.2975,'tooltip':'Jamaica English Jamaican Patois'},
        {'lat':18.2208,'lon':-66.5901,'tooltip':'Puert Rico (Haitian Creole Minority Population)'},
        {'lat':21.5218,'lon':-77.7812,'tooltip':'Cuba (Haitian Creole Minority Population)'}
    ]"""

    return render_template("index.html", markers=location_data)

"""def testing():
    f = open("locations.geojson")
    location_data = json.load(f)

    print(location_data)
testing()"""