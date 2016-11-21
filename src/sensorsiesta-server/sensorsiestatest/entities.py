from datetime import datetime
from pytz import utc
from sensorsiestaserver.entities import Entity


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