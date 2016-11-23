'''
Raspberry client-side application.
Monitors sensors and sends data to a server.
@author Csaba Sulyok
'''

from sensorsiestaclient.broadcast import DataBroadcaster
from sensorsiestaclient.dsp import ExampleDsp


if __name__ == '__main__':
    
    serverHost = 'localhost'
    serverPort = 5000
    period = 1.5
    
    # build sensor dsp object
    dsp = ExampleDsp()
    
    # build and start broadcaster object
    broadcaster = DataBroadcaster(dsp = dsp,
                                  serverHost = serverHost,
                                  serverPort = serverPort,
                                  period = period)
    broadcaster.run()
