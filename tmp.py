from Analyzing.ObjectDocumentModel2 import Denotate,Connection,Relation

with open('txt/denotates.txt') as f:
    ds=[l.replace("\n",'') for l in f.readlines()]

for d in ds:
    c = d.split(';')
    if len(c)>2:
        d1=Denotate(c[0]).save()
        r=Relation(c[1]).save()
        d2=Denotate(c[2]).save()
        w=1
        c = Connection(d1,r,d2,w).save()
