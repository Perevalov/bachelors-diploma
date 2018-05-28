from Analyzing.Denotates import Denotate, Relation,Connection,SubjectArea

class Model:
    def __init__(self,db):
        self.Db=db

    def isExistsInList(self,object,list):
        for o in list:
            if o.Id == object.Id:
                return True
        return False


    def findById(self,id,list):
        for o in list:
            if id == o.Id:
                return o
        return 0

    def getDenotates(self):
        denotates = []
        denotatesDb = self.Db.execute('SELECT * FROM denotate;')
        denotatesDb = self.Db.fetchall()
        denotatesDb = [list(i) for i in denotatesDb]
        for d in denotatesDb:
            den = Denotate(d[0], d[1],
                                   d[2])

            if not self.isExistsInList(den,denotates):
                denotates.append(den)

        return denotates

    def getRelations(self):
        relations = []
        relationsDb = self.Db.execute('SELECT * from relation;')
        relationsDb = self.Db.fetchall()
        relationsDb = [list(i) for i in relationsDb]
        for r in relationsDb:
            rel = Relation(r[0], r[1])

            if not self.isExistsInList(rel, relations):
                relations.append(rel)

        return relations

    def getSubjectAreas(self):
        subjectAreas = []
        subjectAreasDb = self.Db.execute('SELECT * from subject_area;')
        subjectAreasDb = self.Db.fetchall()
        subjectAreasDb = [list(i) for i in subjectAreasDb]
        for s in subjectAreasDb:
            sa = SubjectArea(s[0], s[1])
            if not self.isExistsInList(sa, subjectAreas):
                subjectAreas.append(sa)

        return subjectAreas

    def getConnections(self,denotates,relations):
        connections = []
        connectionsDb =  self.Db.execute('SELECT * from connection;')
        connectionsDb = self.Db.fetchall()
        connectionsDb = [list(i) for i in connectionsDb]

        for c in connectionsDb:
            fromDenotate = self.findById(c[1],denotates)
            relation = self.findById(c[2],relations)
            toDenotate = self.findById(c[3], denotates)
            conn = Connection(c[0],fromDenotate,relation,toDenotate,c[4])
            if fromDenotate != 0 and toDenotate != 0 and relation !=0:
                connections.append(conn)
        return connections

