from pymongo import TEXT
from pymongo.operations import IndexModel
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel

connect('mongodb://localhost:27017/DEV_IDS')

class DenotateType (MongoModel):
    code = fields.CharField(primary_key=True)

class RelationType (MongoModel):
    code = fields.CharField(primary_key=True)

class Denotate(MongoModel):
    name = fields.CharField(primary_key=True)
    definition = fields.CharField()
    type = fields.ReferenceField(DenotateType)

class Relation(MongoModel):
    name = fields.CharField(primary_key=True)
    type = fields.ReferenceField(RelationType)

class Connection(MongoModel):
    denotate1 = fields.ReferenceField(Denotate)
    relation = fields.ReferenceField(Relation)
    denotate2 = fields.ReferenceField(Denotate)
    weight = fields.IntegerField()

#пример создания документов
#term = DenotateType("TERM").save()
#rType = RelationType("IS").save()
#d1 = Denotate("автоматизированная система",term).save()
#r = Relation("это",rType).save()
#d2 = Denotate("система", term).save()
#c = Connection(d1,r,d2,1).save()

#пример получения документов
#cons = Connection.objects

#for c in cons:
    #print(c.denotate1.name)