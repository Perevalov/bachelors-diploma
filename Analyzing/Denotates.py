from fuzzywuzzy import fuzz
import pandas as pd

class Denotate:

    def __init__(self,id,name,subjectAreaId):

        self.Id = id
        self.Name = name
        self.SubjectAreaId = subjectAreaId

    def __repr__(self):
        return '\nДенотат: \nНаименование: {}'.format(self.Name)

class Relation:

    def __init__(self,id,name):

        self.Id = id
        self.Name = name

    def __repr__(self):
        return '\nОтношение: \n Наименование: {}'.format(self.Name)


class Connection:

    def __init__(self,id,fromDenotate,relation,toDenotate,weight):

        self.Id=id
        self.FromDenotate=fromDenotate
        self.Relation=relation
        self.ToDenotate=toDenotate
        self.Weight = weight

    def __repr__(self):
        return 'Связьенотатов: \n Идентификатор: {},\n Денотат 1: {},\n Связь: {},\n Денотат 2:{} \n\n'.format(self.Id,self.FromDenotate,
                                                                                  self.Relation,self.ToDenotate)

    @staticmethod
    def searchByDenotate(denotate,connections):
        foundConnections = []
        isNull = True
        for c in connections:
            if fuzz.ratio(c.FromDenotate.Name, denotate) > 80 or fuzz.ratio(c.ToDenotate.Name, denotate) > 80:
                foundConnections.append(c)
                isNull = False

        if not isNull:
            return foundConnections
        else:
            return 0

class SubjectArea:

    def __init__(self,id,name):
        self.Id=id
        self.Name=name

    def __repr__(self):
        return 'Предметная область - Идентификатор: {}, Наименование: {}'.format(self.Id,self.Name)



    @staticmethod
    def getSubjectAreaByConnections(connections,subjectAreas):
        list = []
        listNames = []
        for cs in connections:
            for c in cs:
                listNames.append(c.FromDenotate.SubjectAreaId)
                listNames.append(c.ToDenotate.SubjectAreaId)
                list.append(c.FromDenotate.SubjectAreaId)
                list.append(c.ToDenotate.SubjectAreaId)

        d = {'name':listNames,'subjectAreaId': list}
        df = pd.DataFrame(data=d)
        return df.groupby(['name']).count().sort_values('subjectAreaId', ascending=False).iloc[0,0]

def findById(id,list):
    for o in list:
        if id == o.Id:
            return o
    return 0

#TODO реализовать поиск связей по денотату и вывод этих связей