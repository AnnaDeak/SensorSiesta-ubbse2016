from datetime import datetime
from pytz import utc

class ExampleEntity(object):
    
    def __init__(self, uid = None, intMember = 42, floatMember = 12.34, dateMember = datetime.now(utc), strMember = 'abc'):
        self.uid = uid
        self.intMember = intMember
        self.floatMember = floatMember
        self.dateMember = dateMember
        self.strMember = strMember