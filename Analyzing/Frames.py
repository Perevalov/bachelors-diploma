from Configuration import Config

class Number:
    def __init__(self,name,amount):

        self.Name = name
        self.Amount = amount

    def __repr__(self):
        return '{} имеет размер {} '.format(self.Name, self.Amount)

class Event:
    def __init__(self,name,date,address):

        self.Name = name
        self.Date = date
        self.Address = address

    def __repr__(self):
        return 'Дата проведения {}: {} '.format(self.Name, self.Date)

class Entity:
    def __init__(self,name,definition):

        self.Name = name
        self.Definition = definition

    def __repr__(self):
        return '{} '.format(self.Definition)

class Place:
    def __init__(self,name,address):

        self.Name = name
        self.Address = address

    def __repr__(self):
        return 'Адрес {}: {} '.format(self.Name, self.Definition)

def fill_frame(connections, type):
    if type == Config.NUMBER:
        numbers = []
        for c in connections:
            if c.relation.name.upper() == Config.AMOUNT_REL:
                amount = c.denotate2.name
                name = c.denotate1.name
                numbers.append(Number(name,amount))
        return numbers
    elif type == Config.DATE:
        events = []
        for c in connections:
            date = ''
            name = ''
            address = ''
            if c.relation.name.upper() == Config.DATE_REL:
                date = c.denotate2.name
                name = c.denotate1.name
                events.append(Event(name, date, address))
            elif c.relation.name.upper() == Config.ADDRESS_REL:
                address = c.denotate2.name
                name = c.denotate1.name
                events.append(Event(name,date,address))
        return events
    elif type == Config.PLACE:
        places = []
        for c in connections:
            name = ''
            address = ''
            if c.relation.name.upper() == Config.ADDRESS_REL:
                address = c.denotate2.name
                name = c.denotate1.name
                places.append(Place(name,address))
        return places
    elif type == Config.DEFINITION:
        entities = []
        for c in connections:
            name = ''
            definition = ''
            if c.relation.name.upper() == Config.DEFINITION_REL or c.relation.name.upper() == Config.UP_REL\
                    or c.relation.name.upper() == Config.DOWN_REL:
                definition = c.denotate2.name
                name = c.denotate1.name
                entities.append(Entity(name,definition))
        return entities

