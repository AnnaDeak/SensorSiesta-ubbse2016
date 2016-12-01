'''
DSP-related classes.
Dummy implementation that can be used for testing.

@author Csaba Sulyok
'''

from random import random


class DummySensorReader(object):
    
    def __init__(self, pin):
        print 'Setting up sensor DSP'
    
    def tearDown(self):
        print 'Tearing down sensor DSP'
    
    def readValue(self):
        return random()
