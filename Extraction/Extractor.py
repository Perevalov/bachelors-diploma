import re, sys,wikipedia,pymorphy2,nltk
from rutermextract import TermExtractor

DEFINITIONS = 'Definitions.txt'
ENDINGS = 'verbEndings.txt'
DELIMITER = '|'
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

def extractTermsAndDefinitions(text):
    term_extractor = TermExtractor()
    sentences = splitTextIntoSentences(text)

    with open(DEFINITIONS, 'r') as myfile:
        relations = myfile.read().replace('\n', '')

    relations = relations.split(DELIMITER)

    for s in sentences:
        if len(term_extractor(s))>0:
            relation = isRelationInString(s, relations)
            if relation != 0:
                for term in term_extractor(s[0:s.find(relation)-1]):
                    print(term.normalized+":::"+s[s.find(relation)+1:len(s)-1])
                    break
                print('====')

def isRelationInString(s,relations):
    for r in relations:
        if r in s:
            return r
    return 0

#def removeAdjectives(text):


def findRelations(text):
    sentences = splitTextIntoSentences(text)
    morph = pymorphy2.MorphAnalyzer()
    term_extractor = TermExtractor()

    with open(ENDINGS, 'r') as myfile:
        endings = myfile.read().replace('\n', '')
    endings = endings.split(DELIMITER)

    for s in sentences:
        words = nltk.word_tokenize(s)
        for w in words:
            if (str(morph.parse(w)[0].tag.POS) == 'VERB' or str(morph.parse(w)[0].tag.POS) == 'ADJS') and (any(w.endswith(e) for e in endings)):
                #print(w+"--"+str(morph.parse(w)[0].tag.POS))
                terms = term_extractor(s[0:s.find(w)-1])
                definitions = term_extractor(s[s.find(w)+1:len(s)-1])
                if len(terms):
                    print(str(terms[0].normalized)+"--"+w+"--"+str(definitions[0].normalized))


findRelations(wikipedia.page("машинное обучение").content)
