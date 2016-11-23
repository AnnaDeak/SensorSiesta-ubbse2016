'''
Entities associated with sensorsiesta project.
@author Csaba Sulyok
'''

from datetime import datetime
from pytz import utc


class Entity(object):
    '''
    General entity which can be used as DB object.
    Must contain UID field.
    All other entities should subclass.
    '''
    
    def __init__(self, uid = None):
        self.uid = uid



class ExampleEntity(Entity):
    '''
    Example entity to be used in tests.
    '''
    
    def __init__(self, uid = None, intMember = 42, floatMember = 12.34, dateMember = datetime.now(utc), strMember = 'abc'):
        Entity.__init__(self, uid)
        self.intMember = intMember
        self.floatMember = floatMember
        self.dateMember = dateMember
        self.strMember = strMember