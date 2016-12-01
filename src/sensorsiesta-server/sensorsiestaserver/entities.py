'''
Entities associated with sensorsiesta project.
@author Csaba Sulyok
'''

from datetime import datetime

from pytz import utc
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, Float, String

from sqlalchemy.orm import relationship
from sensorsiestacommon.entities import Example, ExampleInner, RPi, SensorType, Sensor, SensorReading
from sensorsiestaserver.flasksqlalchemy import Model, TimeZoneAwareDateTime


'''
Example entities
'''

class ExampleEntity(Model, Example):
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
            
            
            
class ExampleInnerEntity(Model, ExampleInner):
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
            
class RPiEntity(Model, RPi):
    uid = Column(Integer, primary_key = True)
    host = Column(String, unique = True)
    sensors = relationship('SensorEntity', backref='rpi', lazy='dynamic', cascade="all, delete-orphan")
    
    def __init__(self, uid = None, host = None):
        self.uid = uid
        self.host = host
    
    def __repr__(self):
        return 'RPi[uid=%d, host=%s, sensors=%s]' %(
            self.uid or 'None', self.host, self.sensors)



class SensorTypeEntity(Model, SensorType):
    uid = Column(Integer, primary_key = True)
    sensors = relationship('SensorEntity', backref='sensorType', lazy='dynamic')
    name = Column(String, unique = True)
    minValue = Column(Float)
    maxValue = Column(Float)
    
    def __init__(self, uid = None, name = None, minValue = 0.0, maxValue = 1.0):
        self.uid = uid
        self.name = name
        self.minValue = minValue
        self.maxValue = maxValue
        
        
    
class SensorEntity(Model, Sensor):
    uid = Column(Integer, primary_key = True)
    rpiUid = Column(Integer, ForeignKey(RPiEntity.uid))
    sensorTypeUid = Column(Integer, ForeignKey(SensorTypeEntity.uid))
    pinNumber = Column(Integer)
    pollInterval = Column(Float)
    readings = relationship('SensorReadingEntity', backref='sensor', lazy='dynamic', cascade="all, delete-orphan")
    
    def __init__(self, uid = None, rpiUid = None, sensorTypeUid = None, pinNumber = -1, pollInterval = 2.0):
        self.uid = uid
        self.rpiUid = rpiUid
        self.sensorTypeUid = sensorTypeUid
        self.pinNumber = pinNumber
        self.pollInterval = pollInterval
    
    def __repr__(self):
        return 'Sensor[uid=%d, sensorTypeUid=%d, pinNumber=%d, pollInterval=%f]' %(
            self.uid or 'None', self.sensorTypeUid, self.pinNumber, self.pollInterval)



class SensorReadingEntity(Model, SensorReading):
    uid = Column(Integer, primary_key = True)
    sensorUid = Column(Integer, ForeignKey(SensorEntity.uid))
    timeOfReading = Column(TimeZoneAwareDateTime)
    value = Column(Float)
    
    def __init__(self, uid = None, sensorUid = None, timeOfReading = datetime.now(utc), value = 0.0):
        self.uid = uid
        self.sensorUid = sensorUid
        self.timeOfReading = timeOfReading
        self.value = value
        
        