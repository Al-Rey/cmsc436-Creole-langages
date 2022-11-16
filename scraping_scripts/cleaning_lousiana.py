# import libraries
import requests
import pandas as pd
import re

from bs4 import BeautifulSoup

# retrieve the data
# letters = "abcdefghijklmnoprstvwyz" # there were no pages for q, u, or x

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

def get_word_data(page_url):
    word_parts = ["n", "v", "adj", "aux", "conj", "prep", "adv", "vphr"]

    raw_data = requests.get(page_url)
    soup = BeautifulSoup(raw_data.content, 'html5lib')
    lang_df = pd.DataFrame(columns=["creole", "english"])
    table = soup.find_all('div', attrs={"class":"entry"})
    # print("length of table:", len(table)) 

    for row in table:
        entry = row.find_all("span", lang=True)
        # print("length of entry:", len(entry))
        # inner loop - parses the data form each page
        saw_split = False
        item = ""
        for val in entry:

            cur_val = val.string
            
            # print(cur_val)
            if cur_val:

                # if there are multiple part of speech labels. This was made an if case to
                # ensure that we don't accidentally come across an actual word with commas in
                # it and assume that it is the part of speech labels
                if "," in cur_val and val["lang"] != "lou":
                    cur_val = cur_val.split(",")
                    for x in cur_val:
                        if x.strip() in word_parts[2:]: 
                            # only check for the parts of speech that is not a verb or a noun. Just because
                            # those are only one letter and they could appear in normal words. You are also not very
                            # likely to find a word that can be both a noun and a verb
                            saw_split = True
                            lang_df.loc[len(lang_df.index), "creole"] = item
                            item = ""
                            break
                    
                    if saw_split:
                        continue
                    else:
                        # end the program if we find an error case
                        print("we found and edge case:", cur_val)
                        exit(0)

                # we don't know if we are loo
                if cur_val not in word_parts and not cur_val.isdigit():
                    if saw_split == True and val["lang"] == "lou":
                        continue
                    item += cur_val
                else:
                    if saw_split == False:
                        saw_split = True
                        lang_df.loc[len(lang_df.index), "creole"] = item
                        item = ""

        item = item.split(";")
        lang_df.loc[len(lang_df.index)-1, "english"] = item
    return lang_df

def parse():
    final_df = pd.DataFrame(columns=["creole", "english"])
    # letters = "abcdefghijklmnoprstvwyz" 
    letters = "abcdef"
    letter_base_url = "https://www.webonary.org/louisiana-creole/browse/browse-vernacular/?letter={}&key=lou"
    base_url = "https://www.webonary.org/louisiana-creole/browse/browse-vernacular/"
    # this would be in the outerloop that loops through the pages on the website

    for letter in letters: #loop through all the valid letters
        print("letter:", letter)
        url = letter_base_url.format(letter)
        raw_html = requests.get(url)
        soup = BeautifulSoup(raw_html.content, 'html5lib')
    
        table = soup.find_all('div', attrs={"id":"wp_page_numbers"})
        page_urls = []
        hold = -1
        if len(table) == 1:
            page_urls = table[0].find_all("a", href=True)
            for index in page_urls:
                new_url = base_url + index["href"]
                hold = get_word_data(new_url)
                print("size of hold:", hold.size)
                # pd.concat([final_df, hold], ignore_index=False)
        elif len(table) == 0:
            hold = get_word_data(url)
            print("size of hold:", hold.size)
        else:
            print("we found an edge case with table size:", len(table))
            exit(0)
        
        pd.concat([final_df, hold], ignore_index=False)

    """
    # table = soup.find_all('div', attrs={"class":"entry"})
    # print("length of table:", len(table)) 

    # for row in table:
    #     entry = row.find_all("span", lang=True)
    #     print("length of entry:", len(entry))
    #     # inner loop - parses the data form each page
    #     saw_split = False
    #     item = ""
    #     for val in entry:

    #         cur_val = val.string
            
    #         # print(cur_val)
    #         if cur_val:

    #             # if there are multiple part of speech labels. This was made an if case to
    #             # ensure that we don't accidentally come across an actual word with commas in
    #             # it and assume that it is the part of speech labels
    #             if "," in cur_val:
    #                 cur_val = cur_val.split(",")
    #                 for x in cur_val:
    #                     if x.strip() in word_parts[2:]: 
    #                         # only check for the parts of speech that is not a verb or a noun. Just because
    #                         # those are only one letter and they could appear in normal words. You are also not very
    #                         # likely to find a word that can be both a noun and a verb
    #                         saw_split = True
    #                         lang_df.loc[len(lang_df.index), "creole"] = item
    #                         item = ""
    #                         break
                    
    #                 if saw_split:
    #                     continue
    #                 else:
    #                     # end the program if we find an error case
    #                     print("we found and edge case:", cur_val)
    #                     exit(0)

    #             # we don't know if we are loo
    #             if cur_val not in word_parts and not cur_val.isdigit():
    #                 if saw_split == True and val["lang"] == "lou":
    #                     continue
    #                 item += cur_val
    #             else:
    #                 if saw_split == False:
    #                     saw_split = True
    #                     lang_df.loc[len(lang_df.index), "creole"] = item
    #                     item = ""

    #     item = item.split(";")
    #     lang_df.loc[len(lang_df.index)-1, "english"] = item   
    """
    print(final_df.head(10))    
    print(final_df.size)


if __name__ == "__main__":
    # testing()
    parse()