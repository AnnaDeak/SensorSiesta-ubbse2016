'''
Entities associated with sensorsiesta project.
@author Csaba Sulyok
'''

from datetime import datetime
from pytz import utc


'''
Example entities
'''

class Example():
    '''
    Example entity to be used in tests.
    '''
    
    def __init__(self, uid = None, intMember = 42, floatMember = 12.34, dateMember = datetime.now(utc), strMember = 'abc'):
        self.uid = uid
        self.intMember = intMember
        self.floatMember = floatMember
        self.dateMember = dateMember
        self.strMember = strMember
        self.inners = []
        
    
    def __repr__(self):
        return 'Example[uid=%d, intMember=%d, floatMember=%f, dateMember=%s, strMember=%s]' %(
            self.uid or 'None', self.intMember, self.floatMember, self.dateMember, self.strMember)
            
            
            
class ExampleInner():
    
    def __init__(self, uid = None, strMember = 'abc'):
        self.uid = uid
        self.strMember = strMember
        
    
    def __repr__(self):
        return 'ExampleInner[uid=%d, strMember=%s]' %(
            self.uid or 'None', self.strMember)



'''
Productive entities
'''
            
class RPi():
    
    def __init__(self, uid = None, host = None):
        self.uid = uid
        self.host = host
        self.sensors = []
    
    def __repr__(self):
        return 'RPi[uid=%d, host=%s, sensors=%s]' %(
            self.uid or 'None', self.host, self.sensors)



class SensorType():
    
    def __init__(self, uid = None, name = None, minValue = 0.0, maxValue = 1.0):
        self.uid = uid
        self.name = name
        self.minValue = minValue
        self.maxValue = maxValue
        self.sensors = []
        
        
    
class Sensor():
    
    def __init__(self, uid = None, rpiUid = None, sensorTypeUid = None, pinNumber = -1, pollInterval = 2.0):
        self.uid = uid
        self.rpiUid = rpiUid
        self.sensorTypeUid = sensorTypeUid
        self.pinNumber = pinNumber
        self.pollInterval = pollInterval
        self.readings = []
        
    
    def __repr__(self):
        return 'Sensor[uid=%d, sensorTypeUid=%d, pinNumber=%d, pollInterval=%.2f]' %(
            self.uid or 'None', self.sensorTypeUid, self.pinNumber, self.pollInterval)



class SensorReading():
    
    def __init__(self, uid = None, sensorUid = None, timeOfReading = datetime.now(utc), value = 0.0):
        self.uid = uid
        self.sensorUid = sensorUid
        self.timeOfReading = timeOfReading
        self.value = value
        
        