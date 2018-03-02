import speech_recognition as sr
from rutermextract import TermExtractor
from fuzzywuzzy import process

r = sr.Recognizer()
term_exctractor = TermExtractor()

def get_matches(query, choises,limit=3):
    results = process.extract(query,choises,limit=limit)
    return results

with sr.Microphone() as source:
    print("Скажите что-нибудь")
    audio = r.listen(source)

try:
    recognized_text = r.recognize_google(audio, language="ru-RU")
    print(recognized_text)

except sr.UnknownValueError:
    print("Робот не расслышал фразу")

except sr.RequestError as e:
    print("Ошибка сервиса; {0}".format(e))

with open('subject_area.txt','r') as f:
    dataset = f.read().split()

for term in term_exctractor (recognized_text):
    print(term.normalized)
    print(get_matches(term.normalized, dataset))


