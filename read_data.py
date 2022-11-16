import json
import csv

##  Global variables to define creole dictionary location and coordinates
CREOLE_LOCATIONS = {"Haitian Creole": [[-72.285,18.9712],[-70.1627,18.7357]], "Jamaican Creole": [[-77.2975,18.1096]], "cayman_creole": [[-81.2546,19.3133]]}
CREOLE_DICTIONARY_LIST = {"Haitian Creole":"scraping_scripts/hatian_creole_dictionary_v3.csv","Jamaican Creole":"scraping_scripts/Jamaican Creole.csv"}
CREOLE_LIST = ["Haitian Creole","Jamaican Creole"]
WORD_NOT_FOUND = "WORD_NOT_FOUND"

#Reading database to find if word appears in creole
def read_database(word,creole):
    with open(CREOLE_DICTIONARY_LIST[creole],'r',newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['word'].rstrip().lower() == word:
                return (row['creole_word'])
    return(WORD_NOT_FOUND)


#Reading database to find which creole languages said creole word appears in
def read_creole(word,creole):
    with open(CREOLE_DICTIONARY_LIST[creole],'r',newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if type(row["creole_word"] == list):
                for sub_word in row["creole_word"]:
                    if sub_word.rstrip().lower() == word:
                        return (sub_word)
            if row['creole_word'].rstrip().lower() == word:
                return (row['word'])
    return(WORD_NOT_FOUND)

#Returns makers if input is creole -> english
def creole_markers(word):
    return


#Returns makers if input is english -> creole
def english_markers(word):
    creole_word = {}
    for creole in CREOLE_LIST:
        temp = read_database(word,creole)
        if temp != WORD_NOT_FOUND:
            creole_word[creole] = temp

    #Creating Python Dictionary in form of geojson to be converted to json later
    creole_dict = {"type":"FeatureCollection","features":[]}
    for creole in creole_word:
        for latlon in CREOLE_LOCATIONS[creole]:
            creole_dict["features"].append(
                {
                "type":"Feature",
                "properties":{"creole_language": creole, "word": word, "creole_word":creole_word[creole]},
                "geometry":{"coordinates":latlon,"type":"Point"}
                })

    #Converting Python Dictionary to Json
    creole_json = json.dumps(creole_dict)

    #Saving Json to locations.json to be read by index.html
    with open("locations.json", "w") as outfile:
        outfile.write(creole_json)
    f = open("locations.json")
    markers = json.load(f)

    return(markers)