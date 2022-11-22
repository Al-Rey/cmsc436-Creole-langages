import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_en_letter_freq(words):
    freq = [0] * 26
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    total_letter_count = 0

    ignore=False
    for word in words:
        if pd.isnull(word):
            continue

        for ch in word:
            if not ignore and ch == '(':
                ignore = True
            elif ignore and ch == ')':
                ignore = False
            elif not ignore:
                index = alphabet.find(ch)

                if index != -1:
                    freq[index] += 1
            total_letter_count += 1
    
    percent_freq = [(x / total_letter_count) * 100 for x in freq]

    return percent_freq




def plot_letter_frequencies(data_df):
    labels = data_df["langauge"].values
    letters = list("abcdefghijklmnopqrstuvwxyz")
    print(data_df.head())
    bar_width = 0.25
    x_axis = np.arange(26)
    counter = 0
    for index, row in data_df.iterrows():
        plt.bar(x_axis + bar_width * counter, row["en_char_freq"], label=row["langauge"], width=bar_width, edgecolor="black")
        counter += 1

    plt.xticks(x_axis + bar_width, letters)
    plt.xlabel("English letters")
    plt.ylabel("Percent of letter occurances")
    plt.title("Frequency of each english character occuring per language")
    plt.legend()
    plt.show()

if __name__ == '__main__':
    # load our data frames
    haitian_df = pd.read_csv("scraping_scripts\hatian_creole_dictionary_v4.csv", index_col=0)
    jamaica_df = pd.read_csv("merging\Jamaican Creole.csv")
    louisiana_df = pd.read_csv("scraping_scripts\louisiana_creole_dictionary.csv", index_col=0)

    # get rid of the columns from each dataframe we don't need to save space
    jamaica_df.drop(columns=["Unnamed: 2", "Country"], inplace=True)
    haitian_df.drop(columns="creole name", inplace=True)
    louisiana_df.drop(columns="creole name", inplace=True)

    # the dataframe with data for the languages themselves
    langauge_df = pd.DataFrame(columns=["langauge", "en_char_freq"])

    langauge_df.loc[len(langauge_df.index), :] = ["louisiana creole", get_en_letter_freq(louisiana_df["creole_word"])]
    langauge_df.loc[len(langauge_df.index), :] = ["jamaican creole", get_en_letter_freq(jamaica_df["Words"])]
    langauge_df.loc[len(langauge_df.index), :] = ["haitian creole", get_en_letter_freq(haitian_df["creole_word"])]
    
    print(langauge_df.head())
    plot_letter_frequencies(langauge_df)