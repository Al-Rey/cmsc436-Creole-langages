import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

from nltk.util import ngrams
from operator import add

COLOR_KEY = { "louisiana": "#a3adb9",
            "haitian" : "#1170aa",
            "jamaican": "#e98629",
            "saramaccan": "#5fa2cd",
            "st lucia": "#c95200",
            "martinique": "#58606d"
            }

TEST_IMG_DIR = "vis_creation\\test_images\\"
IMG_DIR = "vis_Creation/"

CREOLE_NAMES = ["louisiana", "haitian", "jamaican", "saramaccan", "st lucia", "martinique"]

NUM_CREOLES = len(CREOLE_NAMES)

def get_words(og_list):
    pattern_paren = "\(.*\)"
    pattern_per = "…?"
    blacklist = ["kreyol pronunciation"]
    word_list = []

    for entry in og_list:
        temp = re.sub(pattern_paren, "", entry)
        temp = re.sub(pattern_per, "", temp)

        if "," in temp:
            temp = temp.split(",")
            for word in temp:
                if word.lower() not in blacklist:
                    word_list.append(word.lower())

        elif temp.lower() not in blacklist:
            word_list.append(temp.lower())


    return word_list, len(word_list)

"""
Name: create_ngrams
Desc: This function creates n-grams. The user can speciy the number n that will be created (for example, 
if the number 2 is passed, then the function will make bigrams). This function will then count how
many times that bigram occurs else where in our dictionary.
Return: The dictionary where the key is the bigrams and the values are the number of times the
bigrams come up.
"""
def create_ngrams(text, n=1):
    blacklist = [" ", ";", ",", "", "-", "!", "/", ".", "…"] # this is a list of characters to ignore for bigrams
    frequency_dic = {} # the frequency of the n-grams that occur. The n-grams are the keys and the values are the count
    
    for word in text: # loop through all the words present in the 
        if word == np.nan:
            continue
        temp = re.sub(r"\(.*\)", "", word)
        letters = list(temp)
        tokens = [token.lower() for token in letters if token not in blacklist]

        grams = list(ngrams(tokens, n))
        for gram in grams:
            if gram in frequency_dic.keys():
                frequency_dic[gram] += 1
            else:
                frequency_dic[gram] = 1
        
    return frequency_dic

"""
Name: plot_ngrams
Params:
    data_dict - the dictionary with the ngrams and thier frequencies
    creole_name - the name of the creole that the dictionary is from
    graph_color - what color to make the bar graphs
    n - the number of tokens in the ngram
Desc: This function creates the bar charts showing the top 10 most frequent
and least frequent ngrams for the given creole language. It then saves the figure
as a png in the vis_creation folder
Return: None
"""
def plot_ngrams(data_dict, creole_name, graph_color, n):
    # sort the dictionary so the ngrams are in order by letter combination
    sorted_dic = sorted(data_dict.items(), key=lambda x:x[1], reverse=True)
    # labels = list(map(str, [item[0] for item in sorted_dic])) # get the ngram names
    labels = ["".join(item[0]) for item in sorted_dic]
    combo_freq = [item[1] for item in sorted_dic] # get the frequency data

    # get the 10 highest and 10 lowest ngrams
    top_10_values =  combo_freq[:10]
    top_10_labels = labels[:10]
    bottom_10_values = combo_freq[-1:-11:-1]
    bottom_10_labels = labels[-1:-11:-1]

    # get the title of the graphs and the name of the image file the graphs will be saved to
    title1 = ""
    title2 = ""
    file_name = ""
    if n == 1:
        title1 = creole_name + " top 10 most common unigrams"
        title2 = creole_name + " top 10 least common unigrams"
        file_name = creole_name + "_unigram_frequency_graphs.png"
    elif n == 2:
        title1 = creole_name + " top 10 most common bigrams"
        title2 = creole_name + " top 10 least common bigrams"
        file_name = creole_name + "_bigram_frequency_graphs.png"
    elif n == 3:
        title1 = creole_name + " top 10 most common trigrams"
        title2 = creole_name + " top 10 least common trigrams"
        file_name = creole_name + "_trigram_frequency_graphs.png"
    else:
        title1 = creole_name + " top 10 most common " + str(n) + "-grams"
        title2 = creole_name + " top 10 least common " + str(n) + "-grams"
        file_name = creole_name + "_" + str(n) + "gram_frequency_graphs.png"
    
    print(title2)
    print(bottom_10_labels)
    print(title1)
    print(top_10_labels)

    # make the plot with two graphs on it
    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True) # make the plot with two graphs on it
    f.set(figheight=120, figwidth=80)
    f.subplots_adjust(bottom=0.2, top=0.9)

    # make the plot for the 10 most common ngrams
    ax1.bar(top_10_labels, top_10_values, color=graph_color)
    ax1.set_title(title1)
    
    ax1.set_ylabel("frequency")
    ax1.tick_params("x", labelrotation=90)
    ax1.set_xlabel("Letter Combination")
    for i in range(10): # put the frequencies for each ngram above the bars
        ax1.text(i, top_10_values[i] + 1, top_10_values[i], ha = 'center')
    
    # make the plot for the 10 least common ngrams
    ax2.bar(bottom_10_labels, bottom_10_values, color=graph_color)
    for i in range(10):
        ax2.text(i, bottom_10_values[i] + 1, bottom_10_values[i], ha = 'center')
    ax2.set_xlabel("Letter Combination")
    ax2.tick_params("x", labelrotation=90)
    ax2.set_title(title2)
    
    # show the plot and save the viz
    plt.show()
    f.savefig(TEST_IMG_DIR+file_name)

def plot_count_pie(total_list, labels_raw=CREOLE_NAMES):
    # total = sum(total_list)
    labels_list = [word.title().replace(" ", ". ") for word in labels_raw]
    pie_colors = [COLOR_KEY[name] for name in labels_raw]
    
    _, _, autotexts = plt.pie(list(total_list), labels=labels_list, colors=pie_colors, autopct=lambda x: str(round(x, 3)) + "%")
    plt.title("Distribution of Creole Words")
    plt.setp(autotexts, size = 8)
    plt.show() 
    plt.savefig(TEST_IMG_DIR+"creole_pie_plot.png")

def plot_stacked_bars(total, dist, n, include_haitian=True, creoles=CREOLE_NAMES):
    # sort the dictionary so the ngrams are in order by letter combination
    sorted_dic = sorted(total.items(), key=lambda x:x[1], reverse=True)[:10]

    # make the dictionary that will hold the individual frequency data for each creole
    vals = {}
    for name in creoles:
        if name == "haitian" and include_haitian:
            vals[name] = []
        if name != "haitian":
            vals[name] = []

    # populate the dictionary with the frequency data for each individual creole
    count = 0
    for item in sorted_dic:
        k = item[0]
        count += 1
        
        # go though all the creoles that had that letter combindation
        for creole in dist[k].keys():
            # print(creole)
            vals[creole].append(dist[k][creole])
            # vals[creole]

        for val in vals.keys():
            if len(vals[val]) != count:
                vals[val].append(0)

    title = ""
    if n == 1:
        title = "Most Common Unigrams"
        file_name = "most_common_unigrams.png"
    elif n == 2:
        title = "Most Common Bigrams"
        file_name = "most_common_bigrams.png"
    elif n == 3:
        title1 = "Most Common Trigrams"
        file_name = "most_common_trigrams.png"
    else:
        title = "Most Common " + str(n) + "-grams"
        file_name = "most_frequent" + str(n) + "grams.png"

            
    # combos = list(map(str, [item[0] for item in sorted_dic])) # get the ngram names
    labels = ["".join(item[0]) for item in sorted_dic]
    print(labels)
    # plot the stacks
    f = plt.figure()
    f.set_figwidth(10)
    f.set_figheight(6)

    prev = [0] * 10
    for key in vals.keys():
        plt.bar(labels, vals[key], bottom=prev, color=COLOR_KEY[key])
        prev = list(map(add, prev, vals[key]))

    plt.legend([word.title().replace(" ", ". ") for word in vals.keys()], title="Creoles")
    plt.ylabel("Frequency")
    plt.xlabel("Letter Combinations")
    plt.title(title)
    plt.tick_params("x", labelrotation=90)
    plt.savefig(TEST_IMG_DIR+file_name)
    plt.show()

# def get_common_freq()

if __name__ == '__main__':
    # creaoles = ["louisiana", "haitian", "jamaican", "surinam"]
    totals = {}
    for name in CREOLE_NAMES:
        totals[name] = 0

    # load our data frames
    haitian_df = pd.read_csv("merging\hatian_creole_dictionary_v4.csv", usecols=[1])
    jamaica_df = pd.read_csv("merging\Jamaican Creole.csv", usecols=["Words"])
    louisiana_df = pd.read_csv("merging\louisiana_creole_dictionary.csv", usecols=["creole_word"])
    surinam_df = pd.read_csv("merging\suriname.csv", usecols=["Creole_word"])
    lucia_df = pd.read_csv("merging\stLucia.csv", usecols=["Creole_word"])
    mart_df = pd.read_csv("merging\martinique.csv", usecols=["Creole_word"])
    
    # drop any NaN values from the dataframe
    louisiana_df.dropna(inplace=True)
    haitian_df.dropna(inplace=True)
    jamaica_df.dropna(inplace=True)
    surinam_df.dropna(inplace=True)
    lucia_df.dropna(inplace=True)
    mart_df.dropna(inplace=True)
   
    # get the creole words from each dataframe
    words_col_louisiana = louisiana_df.loc[:, "creole_word"].tolist()
    words_col_haitian = haitian_df.loc[:, "creole_word"].tolist()
    words_col_jamaican = jamaica_df.loc[:, "Words"].tolist()
    words_col_surinam = surinam_df.loc[:, "Creole_word"].tolist()
    words_col_lucia = lucia_df.loc[:, "Creole_word"].tolist()
    words_col_mart = mart_df.loc[:, "Creole_word"].tolist()

    words_louisiana, totals["louisiana"] = get_words(words_col_louisiana)
    words_haitian, totals["haitian"] = get_words(words_col_haitian)
    words_jamaican, totals["jamaican"] = get_words(words_col_jamaican)
    words_surinam, totals["saramaccan"] = get_words(words_col_surinam)
    words_lucia, totals["st lucia"] = get_words(words_col_lucia)
    words_mart, totals["martinique"] = get_words(words_col_mart)
    print("lec",len(words_louisiana))
    # get the n-gram data
    n = 2
    louisiana_bigrams = create_ngrams(words_louisiana[:], n) 
    haitian_bigrams = create_ngrams(words_haitian[:], n) 
    jamaican_bigrams = create_ngrams(words_jamaican[:], n) 
    surinam_bigrams = create_ngrams(words_surinam[:], n) 
    lucia_bigrams = create_ngrams(words_lucia[:], n) 
    mart_bigrams = create_ngrams(words_mart[:], n) 

    # print("Louisiana Bigrams")
    # print(louisiana_bigrams)

    # plot the ngrams
    plot_ngrams(louisiana_bigrams, "Louisiana Creole", COLOR_KEY["louisiana"], n)
    plot_ngrams(haitian_bigrams, "Haitian Creole", COLOR_KEY["haitian"], n)
    plot_ngrams(jamaican_bigrams, "Jamaican Creole", COLOR_KEY["jamaican"], n)
    plot_ngrams(surinam_bigrams, "Saramaccan Creole", COLOR_KEY["saramaccan"], n)
    plot_ngrams(lucia_bigrams, "St. Lucia Creole", COLOR_KEY["st lucia"], n)
    plot_ngrams(mart_bigrams, "Martinique Creole", COLOR_KEY["martinique"], n)

    cum_freq = {}
    freq_dist = {}
    i = ()
    # labels = list(map(str, [item[0] for item in sorted_dic]))
    for key in list(louisiana_bigrams.keys()):
        freq_dist[key] = freq_dist.get(key, {})
        freq_dist[key]["louisiana"] = louisiana_bigrams[key]
        cum_freq[key] = cum_freq.get(key, 0) + louisiana_bigrams[key]

    for key in list(haitian_bigrams.keys()):
        freq_dist[key] = freq_dist.get(key, {})
        freq_dist[key]["haitian"] = haitian_bigrams[key]
        cum_freq[key] = cum_freq.get(key, 0) + haitian_bigrams[key]

    for key in list(jamaican_bigrams.keys()):
        # i = key
        freq_dist[key] = freq_dist.get(key, {})
        freq_dist[key]["jamaican"] = jamaican_bigrams[key]
        cum_freq[key] = cum_freq.get(key, 0) + jamaican_bigrams[key]

    for key in list(surinam_bigrams.keys()):
        # i = key
        freq_dist[key] = freq_dist.get(key, {})
        freq_dist[key]["saramaccan"] = surinam_bigrams[key]
        cum_freq[key] = cum_freq.get(key, 0) + surinam_bigrams[key]

    for key in list(lucia_bigrams.keys()):
        # i = key
        freq_dist[key] = freq_dist.get(key, {})
        freq_dist[key]["st lucia"] = lucia_bigrams[key]
        cum_freq[key] = cum_freq.get(key, 0) + lucia_bigrams[key]

    for key in list(mart_bigrams.keys()):
        # i = key
        freq_dist[key] = freq_dist.get(key, {})
        freq_dist[key]["martinique"] = mart_bigrams[key]
        cum_freq[key] = cum_freq.get(key, 0) + mart_bigrams[key]

    plot_stacked_bars(cum_freq, freq_dist, n)
    plot_count_pie(totals.values(), CREOLE_NAMES)