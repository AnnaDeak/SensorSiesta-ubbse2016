'''
Allows broadcast of data through RPyC to server.
Monitors DSP periodically and publishes result.

@author Csaba Sulyok
'''
from time import sleep
from sensorsiestacommon.flaskrestclient import FlaskRestClient
from sensorsiestacommon.async import AsyncObject
import socket


class DataBroadcaster(object):
    '''
    Data broadcasting object.
    Periodically pools sensor information from DSP module
    and calls remote DAO method to publish.
    '''
    
    def __init__(self, dsp, serverHost = 'localhost', serverPort = 5000, period = 1.0):
        self.dsp = dsp
        self.period = period
        
        self.conn = FlaskRestClient(host = serverHost, port = serverPort)
        self.connAsync = AsyncObject(self.conn)
        self.acquireRPi()
        
    
    
    def acquireRPi(self):
        self.host = socket.gethostname()
        
        print 'Check if current host registered:', self.host
        response = self.conn.request(urlname = '/RPis?host=%s' %(self.host))
        
        if len(response['RPis']) > 0:
            self.rpi = response['RPis'][0]
            print 'Found on server, uid = %d' %(self.rpi.uid)
        else:
            print 'Not found on server, creating'
            response = self.conn.request(urlname = '/RPis',
                                    method = 'POST',
                                    host = self.host)
            self.rpi = response['RPi']
            print 'Assigned uid = %d' %(self.rpi.uid)
            
            
        
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
                self.connAsync.request(urlname = '/ExampleEntitys',
                                       method='POST',
                                       **readings.__dict__)
                
                # sleep until next poll
                sleep(self.period)
                
        except KeyboardInterrupt:
            # react to keyboard interrupt
            pass
        finally:
            # make sure teardown happens for graceful exit
            self.dsp.tearDown()
