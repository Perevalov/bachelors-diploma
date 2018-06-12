import pymorphy2
from nltk.corpus import stopwords

morph = pymorphy2.MorphAnalyzer()

yes_no = []
description = []
number = []
place = []
date = []

"""
yes_no
*наречие* ли
*глагол* ли
*числительное* ли
"""
with open('txt/AnswerType/yes_no.txt') as f:
    yes_no=[l.strip() for l in f.readlines()]

with open('txt/AnswerType/description.txt') as f:
    description=[l.strip() for l in f.readlines()]

with open('txt/AnswerType/number.txt') as f:
    number=[l.strip() for l in f.readlines()]

with open('txt/AnswerType/place.txt') as f:
    place=[l.strip() for l in f.readlines()]

with open('txt/AnswerType/date.txt') as f:
    date=[l.strip() for l in f.readlines()]

def yes_no_score(text_list):
    counter = 0
    for word in text_list:
        if any(word == i for i in yes_no):
            counter=counter+1
    return counter/len(text_list)

def description_score(text_list):
    counter = 0
    for word in text_list:
        if any(word == i for i in description):
            counter=counter+1
    return counter/len(text_list)

def number_score(text_list):
    counter = 0
    for word in text_list:
        if any(word == i for i in number):
            counter=counter+1
    return counter/len(text_list)

def place_score(text_list):
    counter = 0
    for word in text_list:
        if any(word == i for i in place):
            counter=counter+1
    return counter/len(text_list)

def date_score(text_list):
    counter = 0
    for word in text_list:
        if any(word == i for i in date):
            counter=counter+1
    return counter/len(text_list)

def classify(s):
    norma = []
    for w in s.split():
        norma.append(morph.parse(w.lower())[0].normal_form)
    vector = [yes_no_score(norma),description_score(norma),number_score(norma),place_score(norma),date_score(norma)]
    return vector







