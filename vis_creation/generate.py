import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

from nltk.util import ngrams
from matplotlib.figure import  Figure

"""
Name: create_ngrams
Desc: This function creates n-grams. The user can speciy the number n that will be created (for example, 
if the number 2 is passed, then the function will make bigrams). This function will then count how
many times that bigram occurs else where in our dictionary.
Return: The dictionary where the key is the bigrams and the values are the number of times the
bigrams come up.
"""
def create_ngrams(text, n=1):
    blacklist = [" ", ";", ",", "", "-", "!", "/", "."] # this is a list of characters to ignore for bigrams
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
    labels = list(map(str, [item[0] for item in sorted_dic])) # get the ngram names
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
    
    # print(bottom_10_labels)
    
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
    f.savefig("vis_Creation/"+file_name)


if __name__ == '__main__':
    # load our data frames
    haitian_df = pd.read_csv("scraping_scripts\hatian_creole_dictionary_v4.csv", index_col=0)
    jamaica_df = pd.read_csv("merging\Jamaican Creole.csv")
    louisiana_df = pd.read_csv("scraping_scripts\louisiana_creole_dictionary.csv", index_col=0)

    # get rid of the columns from each dataframe we don't need to save space
    jamaica_df.drop(columns=["Unnamed: 2", "Country"], inplace=True)
    haitian_df.drop(columns="creole name", inplace=True)
    louisiana_df.drop(columns="creole name", inplace=True)

    # drop any NaN values from the dataframe
    louisiana_df.dropna(inplace=True)
    haitian_df.dropna(inplace=True)
    jamaica_df.dropna(inplace=True)
   
    # get the haitian words from each dataframe
    words_louisiana = louisiana_df.loc[:, "creole_word"].tolist()
    words_haitian = haitian_df.loc[:, "word"].tolist()
    words_jamaican = jamaica_df.loc[:, "Words"].tolist()
    
    # get the bigram data
    n = 3
    louisiana_bigrams = create_ngrams(words_louisiana[:], n) 
    haitian_bigrams = create_ngrams(words_haitian[:], n) 
    jamaican_bigrams = create_ngrams(words_jamaican[:], n) 


    # plot the ngrams
    plot_ngrams(louisiana_bigrams, "Louisiana Creole", "maroon", n)
    plot_ngrams(haitian_bigrams, "Haitian Creole", "green", n)
    plot_ngrams(jamaican_bigrams, "Jamaican Creole", "blue", n)