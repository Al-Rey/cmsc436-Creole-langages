from flask import Flask, render_template
import os

##
## https://medium.com/geekculture/how-to-make-a-web-map-with-pythons-flask-and-leaflet-9318c73c67c3
##


def read_database():
    return 0

app = Flask(__name__)

# Probably don't need more than one webpage, probably just need to update this webpage whenever user selects something
# Non-interactive map
#   1. Get png of the Caribbean
#   2. lat-lon points for country capitals and label them with languages
# Interactive map
#   1. Display blank map of the Caribbean -- probably will use openstreetmaps
#   2. Color different countries different colors
#   3. Allow user selection 
#       3a. Alpha -- select Creole language and display it's location on map 
@app.route('/')
@app.route('/index')
def root():

    markers=[   
        {'lat':19.3133,'lon':-81.2546,'tooltip':'Cayman Islands English Cayman Creole'},
        {'lat':18.7357,'lon':-70.1627,'tooltip':'Dominican Republic Spanish Haitian Creole'},
        {'lat':18.9712	,'lon':-72.2852,'tooltip':'Haiti French Haitian Creole'},
        {'lat':18.1096,'lon':-77.2975,'tooltip':'Jamaica English Jamaican Patois'},
        {'lat':18.2208,'lon':-66.5901,'tooltip':'Puert Rico (Haitian Creole Minority Population)'},
        {'lat':21.5218,'lon':-77.7812,'tooltip':'Cuba (Haitian Creole Minority Population)'}
    ]

    return render_template("index.html", markers=markers)