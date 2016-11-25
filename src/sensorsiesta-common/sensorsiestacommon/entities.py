'''
Entities associated with sensorsiesta project.
@author Csaba Sulyok
'''

from datetime import datetime

from pytz import utc
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, Float, String

from sensorsiestacommon.flasksqlalchemy import Model
from sensorsiestacommon.utils import TimeZoneAwareDateTime


class ExampleEntity(Model):
    '''
    Example entity to be used in tests.
    '''
    uid = Column(Integer, primary_key = True)
    intMember = Column(Integer)
    floatMember = Column(Float)
    dateMember = Column(TimeZoneAwareDateTime)
    strMember = Column(String)
    
    def __init__(self, uid = None, intMember = 42, floatMember = 12.34, dateMember = datetime.now(utc), strMember = 'abc'):
        self.uid = uid
        self.intMember = intMember
        self.floatMember = floatMember
        self.dateMember = dateMember
        self.strMember = strMember
        
        