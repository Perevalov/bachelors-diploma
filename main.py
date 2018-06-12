from Analyzing.Denotates import Connection
from rutermextract import TermExtractor
from graphviz import Digraph
from Analyzing.ObjectDocumentModel import Denotate,Connection,Relation
from Analyzing.ObjectDocumentModel2 import Connection as Conn
from fuzzywuzzy import fuzz
import AnswerTypeClassifier as cls

def getKeyByValue(dict,val):
    for a,b in dict:
        if b==val:
            return a
def main():

    #sd = SpeechDetector()
    #sd.setup_mic()

    #s = sd.run()

    foundConnections = []
    term_extractor = TermExtractor()
    connections = []
    s = "Здравствуйте. Можно подать документы для поступления в электронном виде? Если да, то какие и на какой адрес?"

    for c in Connection.objects.all():
        if any(fuzz.ratio(c.denotate1.name.lower(),str(t.normalized))>80 for t in term_extractor(s,nested=False)):
            print(c.denotate1.name+"--"+c.relation.name+"--"+c.denotate2.name)
            connections.append(c)

    dot = Digraph(comment='connections tree')

    for c in connections:
        dot.node(str(c.denotate1.name),str(c.denotate1.name))
        dot.node(str(c.denotate2.name), str(c.denotate2.name))
        dot.edge(str(c.denotate1.name),str(c.denotate2.name),label=str(c.relation.name))

    print(dot.source)
    dot.render('graphs/round-table.gv')

def IR():
    map = {'yes_no': 0, 'description': 1, 'number': 2, 'place': 3, 'date': 4}
    search_rules = {'ЭТО': 0, 'ЭТО': 1, 'РАЗМЕР': 2, 'АДРЕС': 3, 'ДАТА': 4}
    s = "когда будет день открытых дверей?"
    vector = cls.classify(s)
    index = vector.index(max(vector))
    print(index)

    term_extractor = TermExtractor()
    print([t.normalized for t in term_extractor(s)])

    for c in Conn.objects.all():
        if (any(fuzz.partial_ratio(c.denotate1.name.lower(),str(t.normalized))>80 for t in term_extractor(s)) or \
            any(fuzz.partial_ratio(c.denotate2.name.lower(), str(t.normalized))>80 for t in term_extractor(s))) and \
                any(c.relation.name == key.lower() for key in getKeyByValue(search_rules,index)):
            print(c.denotate1.name + "--" + c.denotate2.name)

IR()
#main()
