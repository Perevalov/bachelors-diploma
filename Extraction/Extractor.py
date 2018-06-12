import re
from fuzzywuzzy import fuzz
from rutermextract import TermExtractor
import xml.etree.ElementTree as ET, wikipedia
from Analyzing.ObjectDocumentModel import Denotate,Connection,Relation
from nltk.tokenize import RegexpTokenizer

wikipedia.set_lang('ru')

def splitTextIntoSentences(text):
    res = []
    regex = re.compile("""
        (?:
            (?:
                (?<!\\d(?:р|г|к))
                (?<!и\\.т\\.(?:д|п))
                (?<!и(?=\\.т\\.(?:д|п)\\.))
                (?<!и\\.т(?=\\.(?:д|п)\\.))
                (?<!руб|коп)
            \\.) |
            [!?\\n]
        )+
        """, re.X)
    sear = regex.search(text)
    while sear:
        res.append(text[:sear.end()])
        text = text[sear.end():]
        sear = regex.search(text)
    if len(text)>10:
        res.append(text)
    return res

def parseRuTez():

    tree = ET.parse('../txt/rutez.xml')
    root = tree.getroot()
    connections = []
    for item in root.iter('item'):
        for rels in item.find('rels'):
            denotate1 = Denotate(item.find('name').text,"no_def")
            relation = Relation(rels[0].text)
            denotate2 = Denotate(rels[1].text, "no_def")
            connection = Connection(denotate1,relation,denotate2,1)
            connections.append(connection)
            #print(item.find('name').text+":"+rels[0].text+":"+rels[1].text)

    return connections

def getWikiPages():

    with open('../txt/article_names.txt') as f:
        names = f.readlines()

    names = [l.strip() for l in names]
    term_extractor = TermExtractor()
    tokens = []

    for name in names:
        print(name)
        tokens = tokens + [term.normalized for term in term_extractor(wikipedia.page(name).content,nested=True)]

    with open('../txt/corpus.txt', 'a') as the_file:
        for t in tokens:
            the_file.write(str(t)+"\n")

def removeDuplicates():
    with open('../txt/corpus.txt') as the_file:
        words = the_file.readlines()
        unique = []
        [unique.append(w) for w in words if (w not in unique and not re.match('[a-z0-9]',w) and len(w)>3)]

    with open('../txt/unique.txt','a') as file:
        for w in unique:
            file.write(str(w))




with open('../txt/unique.txt', 'r') as the_file:
    tokens = the_file.readlines()

cons = parseRuTez()

for c in cons:
    if any(fuzz.ratio(str(c.denotate1.name).lower(),t)>90 for t in tokens) or any(fuzz.ratio(str(c.denotate2.name).lower(),t)>90 for t in tokens):
        print("saved")
        c.denotate1.save()
        c.denotate2.save()
        c.relation.save()
        c.save()


