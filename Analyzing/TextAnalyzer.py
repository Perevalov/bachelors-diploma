import re,pymorphy2
from Configuration import Config
from fuzzywuzzy import fuzz
from rutermextract import TermExtractor
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
    with open('/home/alex/diploma/txt/stopwords.txt') as f:
        stopwords = [l.replace("\n", '') for l in f.readlines()]
    morph = pymorphy2.MorphAnalyzer()
    text = re.sub('[^А-Яа-я]+', ' ', text) # Удаляем все, кроме букв
    text = ''.join(morph.parse(word)[0].normal_form + ' ' for word in text.split()
                   if morph.parse(word)[0].normal_form not in stopwords).strip() #Заполняем строку леммами
    return text

def find_denotate_connections(text):
    all_connections = Conn.objects.all()
    term_extractor = TermExtractor()
    terms = term_extractor(text)  # Термы текста
    connections = [] # Инициализируем список отношений

    for c in all_connections:
        #Сравнение по денотату 1
        if any(fuzz.partial_ratio(c.denotate1.name.lower(),str(t.normalized)) > 70 for t in terms):
            if not isExists(c,connections):
                connections.append(c)
                connections =connections + get_parent(c.denotate1, all_connections)
        #Сравнение по денотату 2
        elif any(fuzz.partial_ratio(c.denotate2.name.lower(), str(t.normalized)) > 70 for t in terms):
            if not isExists(c,connections):
                connections.append(c)
                connections=connections+get_parent(c.denotate2,all_connections)

    #print([c.denotate1.name+"--"+c.denotate2.name for c in connections])
    return connections

def get_parent(denotate,all_connections):
    #Ищем главный денотат

    connections = []
    for c in all_connections:
        if (c.denotate1.name == denotate.name) and (c.relation.name.upper() == Config.ALIAS_REL):
            for c1 in all_connections:
                if (c1.denotate1.name==c.denotate2.name) or (c1.denotate2.name == c.denotate2.name):
                    if not isExists(c1, connections):
                        connections.append(c1)
    return connections

#find_denotates("Здравствуйте. Можно подать документы для поступления в электронном виде?")

