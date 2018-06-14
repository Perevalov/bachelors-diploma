from Analyzing.ObjectDocumentModel2 import Denotate,Connection,Relation

with open('txt/denotates.txt') as f:
    ds=[l.replace("\n",'') for l in f.readlines()]

for d in ds:
    c = d.split(';') #разбиение строки
    if len(c)>2: #проверка на целостность структуры строки
        d1 = Denotate(c[0]).save() #создание и сохранение в БД
        r = Relation(c[1]).save()
        d2 = Denotate(c[2]).save()
        c = Connection(d1,r,d2,1).save()
