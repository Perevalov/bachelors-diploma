from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
import re
from rutermextract import TermExtractor
import speech_recognition as sr
from fuzzywuzzy import process

stop = set(stopwords.words('russian'))

def remove_stop_words(query):
    str = ''
    for i in wordpunct_tokenize(query):
        if i not in stop and len(i)>2:
            str = str + re.sub(r'[).(,]','',i) + ' '

    return str.rstrip().lower()

def get_terms(query):

    term_exctractor = TermExtractor()
    list = [str(term) for term in term_exctractor(query,limit=10,nested=True)]
    return list

def terms_to_string(terms):
    str_terms = ''
    for term in terms:
        str_terms = str_terms + str(term) + ' '
    return  str_terms.rstrip()

def compare_docs(doc1,doc2):
    clean_answer = remove_stop_words(doc1)
    clean_kb = remove_stop_words(doc2)
    terms_answer = get_terms(clean_answer)
    terms_kb = get_terms(clean_kb)

    relevant_terms = []

    for term in terms_answer:
        if len(process.extractBests(term,terms_kb,score_cutoff=65,limit=3)) > 0:
            relevant_terms.append(term)

    for term in relevant_terms:
        print(term)
    return str(len(relevant_terms)/len(terms_kb)*100)

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Дайте определение информатике?")
        audio = r.listen(source)

    try:
        recognized_text = r.recognize_google(audio, language="ru-RU")
        print(recognized_text)
        return recognized_text

    except sr.UnknownValueError:
        print("Робот не расслышал фразу")
        return "NULL"

    except sr.RequestError as e:
        print("Ошибка сервиса; {0}".format(e))
        return "NULL"


answer = 'информатика это наука об информации'
if (answer == "NULL"):
    print('Попробуйте ещё раз')
else:
    res = compare_docs(answer, 'отрасль науки, изучающая структуру и свойства информации, а также вопросы, связанные с ее сбором, хранением, поиском, передачей, переработкой, преобразованием, распространением и использованием в различных сферах человеческой деятельности.  наука о методах и процессах сбора, хранения, обработки, передачи, анализа и оценки информации с применением компьютерных технологий, обеспечивающих возможность её использования для принятия решений ')
    print(res)
