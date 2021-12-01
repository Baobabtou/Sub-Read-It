"""
Analysis of a text without neural network
"""

import matplotlib.pyplot as plt
import pandas as pd
from textblob import TextBlob

# Small utility to get the absolute path to the current module.
from inspect import getsourcefile
from os.path import abspath
import os
path_to_ressources = abspath(getsourcefile(lambda: 0))
path_to_ressources = os.path.join(path_to_ressources, '../../../training_datasets')
path_to_ressources = os.path.normpath(path_to_ressources)
the_path = os.path.join(path_to_ressources,'emotion_data.csv')

def analyze_emotions(text):
    """
    Returns a dictionary of keys = the seven main human emotions (disgust, surprise, neutral, anger, sad, happy, fear) 
    and values = the 'strength' of this emotion in the text. This 'strength' is not a percentage, it is an absolute value: 
    one text can have very few emotions and another all emotions very 'strong'
    """

    text = list(TextBlob(text).word_counts.keys())
    # the words of the dataset are followed by a space so we have to add one at the end of the words of the text
    text = [word+' ' for word in text]
    # opening the dataset of emotions
    f = open(file=the_path)
    emotion_dataset = pd.read_csv(f)
    f.close()

    emotion_list = list(dict(emotion_dataset['word']).values())
    emotion_dataset.set_index("word", inplace=True)

    emotions_in_text = {
        'disgust': 0,
        'surprise': 0,
        'neutral': 0,
        'anger': 0,
        'sad': 0,
        'happy': 0,
        'fear': 0
    }

    for word in text:
        if word in emotion_list:
            for emotion in emotions_in_text.keys():
                emotions_in_text[emotion] += emotion_dataset[emotion][word]

    return emotions_in_text


def analyze_theme(text, precise=True):
    """
    Returns a dictionary of the following form:
    {'proper_names': {'name':'number_of_occurence}, 'categories': {'category':'number_of_occurence'}}
    the 'names' are the proper_names that are found in the text 'text' and the 'categories' are the type of informations
    that are found in the text (names of personalities, of places, of monuments, etc.) 
    This way, it gives very useful informations about the subject and the main themes of a text.
    If argument precise = False, the function only returns the category (in order to be quicker)
    """
    import spacy

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    themes = {'proper_names': {}, 'categories': {}}
    for ent in doc.ents:
        if precise:
            if ent.text not in themes['proper_names'].keys():
                themes['proper_names'][ent.text] = 1
            else:
                themes['proper_names'][ent.text] += 1
        if ent.label_ not in themes['categories'].keys():
            themes['categories'][ent.label_] = 1
        else:
            themes['categories'][ent.label_] += 1
    return(themes)

def select_main(dictionary, n=2):
    """
    Returns a dictionary made up of the n elements of a dictionary of the form: {'str':int, 'str2':int2, ...} which have the greatest values
    (for example, select_main({'a':1,'b':2,'c':3}, n=2) returns {'b':2,'c':3})
    """
    values = list(dictionary.values())
    keys = list(dictionary.keys())
    main = {}
    for i in range(n):
        value_max = max(values)
        index_max = values.index(value_max)
        key_max = keys[index_max]
        main[key_max] = value_max
        values.remove(values[index_max])
        keys.remove(keys[index_max])
    return(main)

def emotion_strength(text):
    """
    returns the total 'emotion strength' of a text: it is an important information because to text can have for example fear as main emotion
    but if the 'emotion strength' of one of them is very small, it means that it doesn't mean a lot, whereas if the emotion strength is 
    very high, it means the text calls on strong emotions. Fake news very often use strong emotions in order to be spread more easily.
    """
    emotions = analyze_emotions(text)
    emotion_strength = 0
    for key in emotions.keys():
        emotion_strength+=emotions[key]
    return(emotion_strength)

if __name__ == '__main__':

    print(select_main(analyze_theme("""Donald John Trump (born June 14, 1946) is the 45th and current president of the United States. Before entering politics, he was a businessman and television personality.
Born and raised in Queens, New York City, Trump attended Fordham University for two years and received a bachelor's degree in economics from the Wharton School of the University of Pennsylvania. He became president of his father Fred Trump's real estate business in 1971, renamed it The Trump Organization, and expanded its operations to building or renovating skyscrapers, hotels, casinos, and golf courses. Trump later started various side ventures, mostly by licensing his name. Trump and his businesses have been involved in more than 4,000 state and federal legal actions, including six bankruptcies. He owned the Miss Universe brand of beauty pageants from 1996 to 2015, and produced and hosted the reality television series The Apprentice from 2004 to 2015.
Trump's political positions have been described as populist, protectionist, isolationist, and nationalist. He entered the 2016 presidential race as a Republican and was elected in a surprise electoral college victory over Democratic nominee Hillary Clinton while losing the popular vote.[a] He became the oldest first-term U.S. president[b] and the first without prior military or government service. His election and policies have sparked numerous protests. Trump has made many false or misleading statements during his campaign and presidency. The statements have been documented by fact-checkers, and the media have widely described the phenomenon as unprecedented in American politics. Many of his comments and actions have been characterized as racially charged or racist. 
""")['proper_names']))