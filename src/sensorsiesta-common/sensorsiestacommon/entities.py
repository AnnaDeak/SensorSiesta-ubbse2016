'''
Entities associated with sensorsiesta project.
@author Csaba Sulyok
'''

from datetime import datetime

from pytz import utc
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, Float, String

from sensorsiestacommon.flasksqlalchemy import Model
from sensorsiestacommon.utils import TimeZoneAwareDateTime
from sqlalchemy.orm import relationship


'''
Example entities
'''

class ExampleEntity(Model):
    '''
    Example entity to be used in tests.
    '''
    uid = Column(Integer, primary_key = True)
    intMember = Column(Integer)
    floatMember = Column(Float)
    dateMember = Column(TimeZoneAwareDateTime)
    strMember = Column(String)
    inners = relationship('ExampleInnerEntity', backref='exampleEntity', lazy='dynamic')
    
    def __init__(self, uid = None, intMember = 42, floatMember = 12.34, dateMember = datetime.now(utc), strMember = 'abc'):
        self.uid = uid
        self.intMember = intMember
        self.floatMember = floatMember
        self.dateMember = dateMember
        self.strMember = strMember
        
    
    def __repr__(self):
        if self.uid is not None:
            return 'ExampleEntity[uid=%d, intMember=%d, floatMember=%f, dateMember=%s, strMember=%s]' %(
                self.uid, self.intMember, self.floatMember, self.dateMember, self.strMember)
        else:
            return 'ExampleEntity[uid=none, intMember=%d, floatMember=%f, dateMember=%s, strMember=%s]' %(
                self.intMember, self.floatMember, self.dateMember, self.strMember)
            
            
            
class ExampleInnerEntity(Model):
    uid = Column(Integer, primary_key = True)
    strMember = Column(String)
    parentUid = Column(Integer, ForeignKey(ExampleEntity.uid))
    
    
    def __init__(self, uid = None, strMember = 'abc'):
        self.uid = uid
        self.strMember = strMember
        
    
    def __repr__(self):
        if self.uid is not None:
            return 'ExampleInnerEntity[uid=%d, strMember=%s]' %(
                self.uid, self.strMember)
        else:
            return 'ExampleInnerEntity[uid=none, strMember=%s]' %(
                self.strMember)



'''
Productive entities
'''
            
class RPi(Model):
    uid = Column(Integer, primary_key = True)
    host = Column(String, unique = True)
    sensors = relationship('Sensor', backref='rpi', lazy='dynamic')
    
    def __init__(self, uid = None, host = None):
        self.uid = uid
        self.host = host



class SensorType(Model):
    uid = Column(Integer, primary_key = True)
    sensors = relationship('Sensor', backref='sensorType', lazy='dynamic')
    name = Column(String, unique = True)
    minValue = Column(Float)
    maxValue = Column(Float)
    
    def __init__(self, uid = None, name = None, minValue = 0.0, maxValue = 1.0):
        self.uid = uid
        self.name = name
        self.minValue = minValue
        self.maxValue = maxValue
        
        
    
class Sensor(Model):
    uid = Column(Integer, primary_key = True)
    rpiUid = Column(Integer, ForeignKey(RPi.uid))
    sensorTypeUid = Column(Integer, ForeignKey(SensorType.uid))
    readings = relationship('SensorReading', backref='sensor', lazy='dynamic')
    
    def __init__(self, uid = None, rpiUid = None, sensorTypeUid = None):
        self.uid = uid
        self.rpiUid = rpiUid
        self.sensorTypeUid = sensorTypeUid



class SensorReading(Model):
    uid = Column(Integer, primary_key = True)
    sensorUid = Column(Integer, ForeignKey(Sensor.uid))
    timeOfReading = Column(TimeZoneAwareDateTime)
    value = Column(Float)
    
    def __init__(self, uid = None, sensorUid = None, timeOfReading = datetime.now(utc), value = 0.0):
        self.uid = uid
        self.sensorUid = sensorUid
        self.timeOfReading = timeOfReading
        self.value = value
        
        