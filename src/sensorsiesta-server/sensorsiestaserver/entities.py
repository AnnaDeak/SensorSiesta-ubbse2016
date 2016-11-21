'''
Entities associated with sensorsiesta project.
@author Csaba Sulyok
'''


class Entity(object):
    '''
    General entity which can be used as DB object.
    Must contain UID field.
    All other entities should subclass.
    '''
    
    def __init__(self, uid = None):
        self.uid = uid
        