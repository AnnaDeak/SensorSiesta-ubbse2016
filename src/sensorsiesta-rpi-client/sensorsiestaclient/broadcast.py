'''
Allows broadcast of data through RPyC to server.
Monitors DSP periodically and publishes result.

@author Csaba Sulyok
'''
from time import sleep
from sensorsiestacommon.flaskrestclient import FlaskRestClient
from sensorsiestacommon.async import AsyncObject
from sensorsiestaclient.acquire import acquireRPi
from sensorsiestaclient.dsp import SensorReaderThread


class DataBroadcaster(object):
    '''
    Data broadcasting object.
    Periodically pools sensor information from DSP module
    and calls remote DAO method to publish.
    '''
    
    def __init__(self, serverHost = 'localhost', serverPort = 5000):
        self.conn = FlaskRestClient(host = serverHost, port = serverPort)
        self.rpi = acquireRPi(self.conn)
        self.connAsync = AsyncObject(self.conn)
        
        self.readerThreads = []
        for sensor in self.rpi.sensors:
            print 'Building reader thread for sensor', sensor.uid
            self.readerThreads.append(SensorReaderThread(sensor, self.connAsync))
        
    
    
    def run(self):
        '''
        Run broadcaster indefinitely until signalled to stop.
        Signalling done by keyboard (ctrl-c)
        '''
        for readerThread in self.readerThreads:
            print 'Starting thread for sensor', readerThread.sensor.uid
            readerThread.start()
    
    
    def join(self):
        '''
        Signals all threads to stop and joins with them.
        '''
        for readerThread in self.readerThreads:
            print 'Joining thread for sensor', readerThread.sensor.uid
            readerThread.exitRequested = True
            
        for readerThread in self.readerThreads:
            readerThread.join()
            