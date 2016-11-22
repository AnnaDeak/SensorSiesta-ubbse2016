'''
Common DSP-related classes.
@author Csaba Sulyok
'''
from random import randint, random
from datetime import datetime
from pytz import utc


class ExampleDsp(object):
    
    def setUp(self):
        print 'Setting up sensor DSP'
    
    def tearDown(self):
        print 'Tearing down sensor DSP'
    
    def readValues(self):
        intMember = randint(0, 255)
        floatMember = random()
        dateMember = datetime.now(utc)
        return {'intMember':intMember, 'floatMember':floatMember, 'dateMember': dateMember}
