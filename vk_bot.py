import time
import vk_api
from graphviz import Digraph
from Analyzing import  TextAnalyzer,Frames
from Configuration import Config
from Analyzing import AnswerTypeClassifier as cls
from Generation import NgramSearch


vk = vk_api.VkApi(token = 'token') #Авторизоваться как сообщество
#vk.auth()
values = {'out': 0,'count': 1,'time_offset': 1}

def getKeyByValue(dict,val):
    for a,b in dict.items():
        if b==val:
            return a

def get_answer(text):
    text = TextAnalyzer.prepare_text(text)
    map = Config.MAP
    vector = cls.classify(text)  # Классифицируем тип ответа
    index = vector.index(max(vector))  # Результат классификации

    # Достаем связки денотатов
    connections = TextAnalyzer.find_denotate_connections(text)

    # Заполняем фреймы
    frames = Frames.fill_frame(connections, getKeyByValue(map, index))

    try:
        if len(frames) > 1:
            if index != 1:
                f = NgramSearch.get_best_frame(text, frames)
                return str(f)
        elif len(frames) > 0:
            return str(frames[0])
    except Exception:
        return "Пожалуйста, переформулируйте свой вопрос."

def write_msg(user_id, s):
    vk.method('messages.send', {'user_id':user_id,'message':s})

while True:
    response = vk.method('messages.get', values)
    if response['items']:
        values['last_message_id'] = response['items'][0]['id']
    for item in response['items']:
            answer = get_answer(item[u'body'])
            print(item[u'body'])
            write_msg(item[u'user_id'],answer)
    time.sleep(1)

