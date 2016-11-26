'''
Raspberry client-side application.
Monitors sensors and sends data to a server.
@author Csaba Sulyok
'''

from sys import argv
from getopt import GetoptError, getopt

from sensorsiestaclient.broadcast import DataBroadcaster
from sensorsiestaclient.dsp import ExampleDsp


def printHelp():
    print '''Raspberry Client for SensorSiesta
---------------------------------

Arguments:
    -h             Print current help information
    -s, --host     Specify host of SensorSiesta server (by default, localhost)
    -p, --port     Specift port of SensorSiesta server (by default, 5000)
    '''
    
    
if __name__ == '__main__':
    
    # default settings
    host = 'localhost'
    port = 5000
    period = 1.5
    
    # parse command-line arguments
    try:
        opts, args = getopt(argv[1:], "hs:p:", ["host=","port="])
    except GetoptError:
        printHelp()
        exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            printHelp()
            exit()
        elif opt in ("-s", "--host"):
            host = arg
        elif opt in ("-p", "--port"):
            port = int(arg)
            
    
    # build sensor dsp object
    dsp = ExampleDsp()
    
    # build and start broadcaster object
    broadcaster = DataBroadcaster(dsp = dsp,
                                  serverHost = host,
                                  serverPort = port,
                                  period = period)
    broadcaster.run()
