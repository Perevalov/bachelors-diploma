from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
import re, json, subprocess, os
from rutermextract import TermExtractor
from fuzzywuzzy import process
from pocketsphinx import LiveSpeech
from os import environ, path
import pyaudio,time,signal

def speak(string):
    os.system("echo "" "+string+" "" | RHVoice-test -p Elena")

def remove_stop_words(query): #удаляем все лишние слова из строки
    stop = set(stopwords.words('russian'))
    str = ''
    for i in wordpunct_tokenize(query):
        if i not in stop and len(i)>2:
            str = str + re.sub(r'[).(,]','',i) + ' '

    return str.rstrip().lower()

def get_terms(query): #вытаскиваем список термов из строки
    term_exctractor = TermExtractor()
    list = [str(term) for term in term_exctractor(query,limit=10,nested=True)]
    return list

def terms_to_string(terms): #преобразуем список термов в строку
    str_terms = ''
    for term in terms:
        str_terms = str_terms + str(term) + ' '
    return  str_terms.rstrip()

def compare_docs(doc1,doc2): #сравниваем
    clean_answer = remove_stop_words(doc1)
    clean_kb = remove_stop_words(doc2)
    terms_answer = get_terms(clean_answer)
    terms_kb = get_terms(clean_kb)

    relevant_terms = []

    for term in terms_answer:
        if len(process.extractBests(term,terms_kb,score_cutoff=65)) > 0: #если терм ученика релевантен по отношению к базе знаний
            relevant_terms.append(term)

    #for term in relevant_terms:
       # print(term)
    if (len(relevant_terms) > len(terms_kb)):
        return 100
    else:
        return str(len(relevant_terms)/len(terms_kb)*100)

def initialize_live_speech():
    speech = LiveSpeech(
        verbose=False,
        sampling_rate=16000,
        buffer_size=2048,
        no_search=False,
        full_utt=False,
        hmm='/home/alex/speech/adapting/ru-ru-kb1',
        lm='/home/alex/speech/adapting/ru_kb.lm',
        dic='/home/alex/speech/adapting/ru_kb.dic'
    )
    return speech

def live_speech_test():
    speech = LiveSpeech(
        verbose=False,
        sampling_rate=16000,
        buffer_size=2048,
        no_search=False,
        full_utt=False,
        hmm='/home/alex/speech/adapting/ru-ru-kb',
        lm='/home/alex/speech/adapting/ru_kb.lm',
        dic='/home/alex/speech/adapting/ru_kb.dic'
    )
    for phrase in speech:
        print(phrase)

def main():

    answer_results_list = []

    speech = initialize_live_speech()

    with open('questions.txt') as json_file: #читаем JSON с вопросами
        questions_list = json.load(json_file)

    counter = 0

    while (counter < len(questions_list['questions'])):

        print(questions_list['questions'][counter]['question'])  # задаем вопрос

        for phrase in speech:
            recognized_answer = str(phrase)
            print(recognized_answer)
            if len(recognized_answer) > 10:
                break

        time.sleep(2)
        if (recognized_answer == ""):
            print('Попробуйте ещё раз')

        else:
            res = compare_docs(recognized_answer, questions_list['questions'][counter]['answer'])  # сравниваем ответ
            answer_results_list.append(res)  # записываем результат в массив
            counter = counter + 1

    for res in answer_results_list:
        print(res)
    print("------- Средний балл в %: --------")
    #print(sum(res)/len(res))

#TODO - prepare acoustic model

live_speech_test()



