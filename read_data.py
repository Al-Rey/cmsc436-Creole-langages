import json
import csv
import ast

##  Global variables to define creole dictionary location and coordinates
TEMP = open("location_point.json")
CREOLE_LOCATIONS = json.load(TEMP)

CREOLE_DICTIONARY_LIST = {"Haitian Creole":"scraping_scripts/hatian_creole_dictionary_v4.csv",
    "Jamaican Creole":"scraping_scripts/Jamaican Creole.csv",
    "Louisiana Creole":"scraping_scripts/louisiana_creole_dictionary.csv",
    "Martinique Antillean Creole":"scraping_scripts/Excelmartinique.csv",
    "Antillean Creole":"scraping_scripts/stLucia.csv",
    "Suriname Saramaccan Creole":"scraping_scripts/suriname.csv",
    "Nigerian Pidgin English":"scraping_scripts/nigeria.csv"
}
CREOLE_LIST =  ["Haitian Creole","Jamaican Creole","Louisiana Creole","Martinique Antillean Creole",
    "Antillean Creole","Suriname Saramaccan Creole","Nigerian Pidgin English"]

ACROLECT_LIST = {"Haitian Creole":"French","Jamaican Creole":"English","Louisiana Creole":"French",
    "Martinique Antillean Creole":"French","Antillean Creole":"French","Suriname Saramaccan Creole":"English-Portugese",
    "Nigerian Pidgin English":"English"}

WORD_NOT_FOUND = "WORD_NOT_FOUND"

#Reading database to find if word appears in creole
def read_database(word,creole):
    with open(CREOLE_DICTIONARY_LIST[creole],'r',newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if "[" in row['word']:
                for sub_word in ast.literal_eval(row["word"]):
                    if sub_word.rstrip().lstrip().lower() == word.rstrip().lstrip().lower():
                        return(row['creole_word'])
            if "," in row['word']:
                comma_word = row['word'].split()
                for sub_word in comma_word:
                    if sub_word.rstrip().lstrip().lower().replace(",","") == word.rstrip().lstrip().lower():
                        return(row['creole_word'])
            if row['word'].rstrip().lstrip().lower() == word.rstrip().lstrip().lower():
                return (row['creole_word'])
    return(WORD_NOT_FOUND)


#Reading database to find which creole languages said creole word appears in
#Reads Creole -- Returns English
def read_creole(word,creole):
    with open(CREOLE_DICTIONARY_LIST[creole],'r',newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if "[" in row['creole_word']:
                for sub_word in ast.literal_eval(row["creole_word"]):
                    if sub_word.rstrip().lstrip().lower() == word.rstrip().lstrip().lower():
                        return(row['word'])
            if "," in row['creole_word']:
                comma_word = row['creole_word'].split()
                for sub_word in comma_word:
                    if sub_word.rstrip().lstrip().lower().replace(",","") == word.rstrip().lstrip().lower():
                        return(row['word'])
            if row['creole_word'].rstrip().lstrip().lower() == word.rstrip().lstrip().lower():
                return (row['word'])
    return(WORD_NOT_FOUND)

#Returns makers if input is creole -> english
def creole_markers(word):
    english_word = {}
    for creole in CREOLE_LIST:
        temp = read_creole(word,creole) #temp = english word
        if temp != WORD_NOT_FOUND:
            english_word[creole] = temp # english_word["haitian"] = "hello"

    english_dict = {"type":"FeatureCollection","features":[]}
    for creole in english_word:
        for latlon in CREOLE_LOCATIONS[creole]:
            english_dict["features"].append(
                {
                "type":"Feature",
                "properties":{"creole_language": creole, "word": english_word[creole], 
                    "creole_word":word,"acrolect": ACROLECT_LIST[creole]},
                "geometry":{"coordinates":latlon,"type":"Point"}
                })

    #Converting Python Dictionary to Json
    english_json = json.dumps(english_dict)

    #Saving Json to locations.json to be read by index.html
    with open("locations.json", "w") as outfile:
        outfile.write(english_json)
    f = open("locations.json")
    markers = json.load(f)

    return(markers)


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
                "properties":{"creole_language": creole, "word": word, 
                    "creole_word":creole_word[creole],"acrolect": ACROLECT_LIST[creole]},
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