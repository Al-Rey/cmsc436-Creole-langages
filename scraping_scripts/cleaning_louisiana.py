# import libraries
import requests
import pandas as pd

from bs4 import BeautifulSoup

"""
This function was soley used to test logic. it does not serve any purpose in the parsing of the data
"""
def testing():
    word_parts = ["n", "v", "adj", "aux", "conj", "prep"]
    test_df = pd.DataFrame(columns=["creole", "english"])
    raw_page = requests.get("https://www.webonary.org/louisiana-creole/browse/browse-vernacular/?letter=a&key=lou")
    soup = BeautifulSoup(raw_page.content, 'html5lib')

    table = soup.find_all('div', attrs={"class":"entry"}) 
    entry = table[0].find_all("span", lang=True)
    # table[0]
    
    saw_split = False
    item = ""
    for x in entry:
        cur_val = x.string
        
        print(x.string)
        if cur_val:
            if cur_val not in word_parts and not cur_val.isdigit():
                item += cur_val
            else:
                if saw_split == False:
                    saw_split = True
                    test_df.loc[len(test_df.index), "creole"] = item
                    item = ""

    item = item.split(";")
    test_df.loc[len(test_df.index)-1, "english"] = item    
            
    print(test_df.head())

"""
This function parses all the word data from a given URLs webpage and returns a dataframe with all the word data
"""
def get_word_data(page_url):
    parts_of_speech = ["n", "v", "adj", "aux", "conj", "prep", "adv", "vphr"] # all of these are the parts of speech indicators present in on the site

    raw_data = requests.get(page_url) # get the HTML of the url passed in
    soup = BeautifulSoup(raw_data.content, 'html5lib') # parse the HTML data with BeautifulSoup
    lang_df = pd.DataFrame(columns=["creole_word", "word", "creole name"]) # The dataframe we will be holding all the word data for this page
    
    table = soup.find_all('div', attrs={"class":"entry"}) # only get the part of the page that has the words

    for row in table: # iterate through all the sections found with the class "entry"
        entry = row.find_all("span") # all the word data are enclosed with "span" tags

        # inner loop - parses the data form each page
        saw_split = False # lets us know when we are looking at the english words of the creole words
        item = "" # this variable will build the words/phrases for each column (creole and english)
        
        for val in entry: # iterate through all the entries enclosed with "span"

            cur_val = val.string # get the string value that is enclosed within these brackets
            
            # if we are looking at something wth the "lang" attribute, then it is going to likely have an english or creole word
            if val.has_attr("lang"): 
                cur_val = val.string
                
                # if the string is empty ignore it
                if not cur_val: 
                    continue

                # if we are looking at a number, then ignore it (the site put number next to repeated words)
                if not cur_val.isdigit(): 
                    
                    # we shouldn't see anything labled as a creole if we saw the divide between the two langauges. 
                    # If we do then they are alternate spellings and we can ignore them for now
                    if saw_split == True and val["lang"] == "lou": 
                        print("Extra Creole word:", cur_val)
                        continue
                    
                    # if there is a comma we may be looking at a list of "parts of speech" indicators
                    if "," in cur_val and val["lang"] != "lou": 
                        saw = False # tells us if any of the words/letters found in the array is a "part of speech" indicator
                        cur_val = cur_val.split(",")# make an array split at the comma
                        
                        # iterate through the array made by splitting at the comma
                        for x in cur_val: 

                            # check if the current ite from the array is in the array for "parts of speech"
                            if x.strip() in parts_of_speech: 
                                saw = True

                                # if we see this and the indicator isn't already set, then set it and start to process the other data
                                if saw_split == False: 
                                    saw_split = True
                                    lang_df.loc[len(lang_df.index), "creole_word"] = item # add the curent state of item to the creole column
                                    item = ""
                                
                                break
                        
                        # if we didn't see a "part of speech" indicator, then print what we found for debuggin purposes
                        if not saw: 
                            print(cur_val)
                            cur_val = "".join(cur_val) # put the arary back together
                        
                        # if we did see something, then we did everything we needed to do, so we can continue with the next "span" value
                        else: 
                            continue

                    # if the value of cur_val is not a part of speech indicator, then append it to the current value of item
                    if cur_val not in parts_of_speech:
                        item += cur_val
                        
            # if the looking at something with a class attribute, then we only care about it if the class is "partofspeech". If it does and the indidicator
            # for the split between creole and english hasn't been set yet, then set it and add the current value of item to the "creole" column of the dataframe
            elif val.has_attr("class"):
                if val["class"] == ["partofspeech"] and saw_split == False:
                    saw_split = True
                    lang_df.loc[len(lang_df.index), "creole_word"] = item
                    item = ""

        # if we get here then we are looking at the english words. If there is more than one english translation for a creole word, it is separated by
        # a semicolon(;). So we make a list, splitting at the semicolon, to represent the various translations. Then we add that to the dataframe under
        # the "english" column
        item = item.split(";")
        lang_df.loc[len(lang_df.index)-1, "word"] = item
        lang_df.loc[len(lang_df.index)-1, "creole name"] = "Louisiana Creole"

    return lang_df # return the final dataframe

"""
This is function is the main funciton that does the parsing of the HTML and determines if there are any other pages per letter that we need to look at.
When you went to some of the pages for each letter there were the little menues at the bottom for page 1, 2, 3, etc. This part of the parsing determines if
Those exist for each letter page, and parses the page according to that.
"""
def parse():
    final_df = pd.DataFrame(columns=["creole_word", "word", "creole name"]) # the dataframe we will be storing all our words in
    letters = "abcdefghijklmnoprstvwyz" # the website has pages for these letters

    letter_base_url = "https://www.webonary.org/louisiana-creole/browse/browse-vernacular/?letter={}&key=lou" # the URL for each letter's landing page
    base_url = "https://www.webonary.org/louisiana-creole/browse/browse-vernacular/" # the first half of the site's URL
    
    # this would be in the outerloop that loops through the pages on the website
    for letter in letters: #loop through all the valid letters
        print("letter:", letter) # print in the console what letter we are on
        
        url = letter_base_url.format(letter) # make the link to get the base letter page
        raw_html = requests.get(url) # get the raw HTML from the site link we just made
        soup = BeautifulSoup(raw_html.content, 'html5lib') # parse the HTML using BeautifulSoup
    
        page_nums = soup.find_all('div', attrs={"id":"wp_page_numbers"}) # get the section of the webpage that would have the page number menu
        page_urls = [] # this array will store the end of the urls for each page that the letter has
        hold = -1

        if len(page_nums) == 1: # there should be only one div section named "wp_page_numbers"
            page_urls = page_nums[0].find_all("a", href=True) # get all the urls for the pages
            
            for index in page_urls: # iterate through the URLs for each page
                new_url = base_url + index["href"]
                hold = get_word_data(new_url) # get the dataframe of all the words on the page

                final_df = pd.concat([final_df, hold], ignore_index=False) # merge the dataframe we just made into the main dataframe we are storing all the word data
        
        elif len(page_nums) == 0: # if there are no sections with the ID "wp_page_numbers" then that means that there is only that one page
            hold = get_word_data(url) # get the dataframe for all the word data on the page
            
            final_df = pd.concat([final_df, hold], ignore_index=False)
        
        else: # if we get here then something went wrong
            print("we found an edge case with number of pages:", len(page_nums))
            exit(0)
        
    # print statements for the user
    # copy = final_df.copy()
    print(final_df.head(10))    
    print(final_df.size)

    final_df.to_csv("louisiana_creole_dictionary.csv") # convert the dataframe to a CSV file
    # copy.to_json("lousiana_creole_dictionary.json") # this doesn't want to work for some reason :/


if __name__ == "__main__":
    # testing()
    parse()