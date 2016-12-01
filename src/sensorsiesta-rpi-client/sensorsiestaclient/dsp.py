'''
Switch dsp import based on machine type.
Raspberry Pis use real sensor reading impl, while other platforms get a dummy implementation.
'''

import platform
from time import sleep
from sensorsiestacommon.entities import SensorReading
from threading import Thread
from pytz import utc
from datetime import datetime


if platform.machine() == 'armv7l':
    from sensorsiestaclient.dsprpi import ActualSensorReader as SensorReader
else:
    from sensorsiestaclient.dspdummy import DummySensorReader as SensorReader


class SensorReaderThread(Thread):
    
    def __init__(self, sensor, connAsync):
        Thread.__init__(self)
        self.sensor = sensor
        self.connAsync = connAsync
        self.sensorReader = SensorReader(self.sensor.pinNumber)
        
        
    def run(self):
        '''
        Run the sensor reader
        '''
        self.exitRequested = False
        
        while not self.exitRequested:
            # read values from dsp
            value = self.sensorReader.readValue()
            
            # build reading object
            reading = SensorReading(sensorUid = self.sensor.uid, timeOfReading = datetime.now(utc), value = value)
            
            # broadcast to dao
            print 'Sensor %s broadcasting %.2f to server' %(self.sensor.uid, value)
            self.connAsync.request(urlname = '/SensorReadings',
                                   method='POST',
                                   **reading.__dict__)
            
            # sleep until next poll
            sleep(self.sensor.pollInterval)
                
        # tear down before exiting
        self.sensorReader.tearDown()