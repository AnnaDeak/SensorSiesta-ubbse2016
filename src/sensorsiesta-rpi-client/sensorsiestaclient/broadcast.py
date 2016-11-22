'''
Allows broadcast of data through RPyC to server.
Monitors DSP periodically and publishes result.

@author Csaba Sulyok
'''
from time import sleep


class DataBroadcaster(object):
    '''
    Data broadcasting object.
    Periodically pools sensor information from DSP module
    and calls remote DAO method to publish.
    '''
    
    def __init__(self, dao, dsp, period = 1.0):
        self.dao = dao
        self.dsp = dsp
        self.period = period
    
    
    def run(self):
        '''
        Run broadcaster indefinitely until signalled to stop.
        Signalling done by keyboard (ctrl-c)
        '''
        self.dsp.setUp()
        
        try:
            while True:
                # read values from dsp
                readings = self.dsp.readValues()
                
                # broadcast to dao
                print 'Broadcasting following data to server:', readings
                self.dao.createByValues(**readings)
                
                # sleep until next poll
                sleep(self.period)
                
        except KeyboardInterrupt:
            # react to keyboard interrupt
            pass
        finally:
            # make sure teardown happens for graceful exit
            self.dsp.tearDown()
