from Analyzing.Model import Model
from Analyzing.Denotates import Connection
from rutermextract import TermExtractor
from pymongo import MongoClient
from graphviz import Digraph
from SpeechDetector import SpeechDetector
import sqlite3


def main():
    Translist = list()
    conn = sqlite3.connect('DB/DEV_IDS')
    c = conn.cursor()

    m = Model(c)
    denotates = m.getDenotates()

    relations = m.getRelations()

    subjectAreas = m.getSubjectAreas()
    connections = m.getConnections(denotates, relations)

    #sd = SpeechDetector()
    #sd.setup_mic()

    s = "расскажи про электротехнический факультет" #sd.run()
    foundConnections = []
    term_extractor = TermExtractor()

    for term in term_extractor(s,nested=True):
        foundConnection = Connection.searchByDenotate(term.normalized,connections)
        if foundConnection != 0:
            foundConnections.append(foundConnection)


    dot = Digraph(comment='connections tree')

    for cons in foundConnections:
        for cs in cons:
            dot.node(str(cs.FromDenotate.Id),str(cs.FromDenotate.Name))
            dot.node(str(cs.ToDenotate.Id), str(cs.ToDenotate.Name))
            dot.edge(str(cs.FromDenotate.Id),str(cs.ToDenotate.Id),label=str(cs.Relation.Name))

    print(dot.source)
    dot.render('graphs/round-table.gv')

    #subjectAreaId = SubjectArea.getSubjectAreaByConnections(foundConnections,subjectAreas)

def test_db():
    client = MongoClient(port=27017)
    db = client.DEV_IDS
    #db.relation.inser({"name":"состоит из","code":"CONTAINS"})


main()
