import re,pymorphy2
from Configuration import Config
from Analyzing import Frames
from fuzzywuzzy import fuzz
from rutermextract import TermExtractor
from Analyzing import AnswerTypeClassifier as cls
from Analyzing.ObjectDocumentModel2 import Connection as Conn

def getKeyByValue(dict,val):
    for a,b in dict.items():
        if b==val:
            return a

def isExists(conn,connections):
    for c in connections:
        if c.denotate1.name==conn.denotate1.name and c.denotate2.name == conn.denotate2.name:
            return True
    return False

def prepare_text(text):
    with open('../txt/stopwords.txt') as f:
        stopwords = [l.replace("\n", '') for l in f.readlines()]
    morph = pymorphy2.MorphAnalyzer()
    text = re.sub('[^А-Яа-я]+', ' ', text) # Удаляем все, кроме букв
    text = ''.join(morph.parse(word)[0].normal_form + ' ' for word in text.split()
                   if morph.parse(word)[0].normal_form not in stopwords).strip() #Заполняем строку леммами
    return text

def find_denotates(text):
    text = prepare_text(text)
    map = Config.MAP
    all_connections = Conn.objects.all()
    term_extractor = TermExtractor()
    vector = cls.classify(text) # Классифицируем тип ответа
    index = vector.index(max(vector)) # Результат классификации
    text = term_extractor(text,nested=True)  # Термы текста
    connections = [] # Инициализируем список отношений

    for c in all_connections:
        if any(fuzz.partial_ratio(c.denotate1.name.lower(),str(t.normalized)) > 80 for t in text):
            if not isExists(c,connections):
                connections.append(c)
                connections + get_parent(c.denotate2, all_connections)
        elif any(fuzz.partial_ratio(c.denotate2.name.lower(), str(t.normalized)) > 80 for t in text):
            if not isExists(c,connections):
                connections.append(c)
                connections+get_parent(c.denotate2,all_connections)

    frame = Frames.fill_frame(connections,getKeyByValue(map,index))

    if len(frame)>1:
        for f in frame:
            print(f)
        print("Если вас не удовлетворяют результаты, пожалуйста, уточните вопрос.")
    elif len(frame)>0:
        print(frame[0])

def get_parent(denotate,all_connections):
    #Ищем главный денотат
    connections = []
    for c in all_connections:
        if (c.denotate1.name == denotate.name) and (c.relation.name == Config.ALIAS_REL):
            for c1 in all_connections:
                if (c1.denotate1.name==c.denotate2.name) and (c1.denotate2.name==c.denotate2.name):
                    connections.append(c)
    return connections

find_denotates("Сколько баллов добавляют за аттестат с отличием?")

