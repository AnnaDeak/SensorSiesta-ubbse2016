'''
DSP-related classes.
Production implementation that can be used on RPis.

@author Csaba Sulyok
'''

from random import random


class ActualSensorReader(object):
    '''
    TODO INCLUDE RPI CODE HERE
    '''
    
    def __init__(self, pin):
        print 'Setting up sensor DSP'
    
    def tearDown(self):
        print 'Tearing down sensor DSP'
    
    def readValue(self):
        return random()
