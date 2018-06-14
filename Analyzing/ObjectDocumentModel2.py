from pymongo import TEXT
from pymongo.operations import IndexModel
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel

connect('mongodb://localhost:27017/DEV_PNRPU')

class Denotate(MongoModel):
    name = fields.CharField(primary_key=True)
    #type = fields.CharField()
    class Meta:
        final = True


class Relation(MongoModel):
    name = fields.CharField(primary_key=True)

    class Meta:
        final = True

class Connection(MongoModel):
    denotate1 = fields.ReferenceField(Denotate)
    relation = fields.ReferenceField(Relation)
    denotate2 = fields.ReferenceField(Denotate)
    weight = fields.IntegerField()

    class Meta:
        final = True
    def __repr__(self):
        return '{} ---> {} ---> {}'.format(self.denotate1,self.relation,self.denotate2)



#пример создания документов
#r = Relation("это",rType).save()
#d2 = Denotate("система", term).save()
#c = Connection(d1,r,d2,1).save()

#пример получения документов
#cons = Connection.objects

