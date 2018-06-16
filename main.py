from graphviz import Digraph
from Analyzing import  TextAnalyzer,Frames
from Configuration import Config
from Analyzing import AnswerTypeClassifier as cls
from Generation import NgramSearch
from  Recognition import SpeechDetector
import os

def getKeyByValue(dict,val):
    for a,b in dict.items():
        if b==val:
            return a
def main():
    s = "Здравствуйте. Можно подать документы для поступления в электронном виде? Если да, то какие и на какой адрес?"

    dot = Digraph(comment='connections tree')

    #for c in connections:
    #    dot.node(str(c.denotate1.name),str(c.denotate1.name))
     #   dot.node(str(c.denotate2.name), str(c.denotate2.name))
      #  dot.edge(str(c.denotate1.name),str(c.denotate2.name),label=str(c.relation.name))

    print(dot.source)
    dot.render('graphs/round-table.gv')

def test(text):
    sd = SpeechDetector.SpeechDetector()
    sd.setup_mic()
    s = sd.run()

    return
    #классифицируем тип ответа
    text = TextAnalyzer.prepare_text(text)
    map = Config.MAP
    vector = cls.classify(text)  # Классифицируем тип ответа
    index = vector.index(max(vector))  # Результат классификации

    #Достаем связки денотатов
    connections = TextAnalyzer.find_denotate_connections(text)

    #Заполняем фреймы
    frames = Frames.fill_frame(connections, getKeyByValue(map, index))

    try:
        if len(frames) > 1:
            if index != 1:
                f = NgramSearch.get_best_frame(text,frames)
                NgramSearch.speak(str(f))
            else:
                [NgramSearch.speak(str(f)) for f in frames]
        elif len(frames) > 0:
            NgramSearch.speak(frames[0])
    except Exception:
        print("Пожалуйста, переформулируйте свой вопрос.")
test("Какие документы необходимо подавать для поступления?")
