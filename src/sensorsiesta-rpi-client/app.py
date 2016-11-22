'''
Raspberry client-side application.
Monitors sensors and sends data to a server.
@author Csaba Sulyok
'''

import rpyc
from sensorsiestaclient.broadcast import DataBroadcaster
from sensorsiestaclient.dsp import ExampleDsp


if __name__ == '__main__':
    
    serverHost = 'localhost'
    serverPort = 8000
    
    # establish connection to server and retrieve dao object
    conn = rpyc.connect(serverHost, serverPort)
    dao = conn.root
    
    # build sensor dsp object
    dsp = ExampleDsp()
    
    # build and start broadcaster object
    broadcaster = DataBroadcaster(dao = dao, dsp = dsp)
    broadcaster.run()
