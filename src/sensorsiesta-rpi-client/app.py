'''
Raspberry client-side application.
Monitors sensors and sends data to a server.
@author Csaba Sulyok
'''

from sys import argv
from getopt import GetoptError, getopt

from sensorsiestaclient.broadcast import DataBroadcaster
from sensorsiestacommon.utils import isPortListening
from time import sleep


def printHelp():
    print '''Raspberry Client for SensorSiesta
---------------------------------

Arguments:
    -h, --help     Print current help information
    -s, --host     Specify host of SensorSiesta server (by default, localhost)
    -p, --port     Specify port of SensorSiesta server (by default, 5000)
    '''
    
    
if __name__ == '__main__':
    
    # default settings
    host = 'localhost'
    port = 5000
    
    # parse command-line arguments
    try:
        opts, args = getopt(argv[1:], 'hs:p:', ['help', 'host=', 'port='])
    except GetoptError:
        printHelp()
        exit(2)
    
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            printHelp()
            exit()
        elif opt in ('-s', '--host'):
            host = arg
        elif opt in ('-p', '--port'):
            port = int(arg)
            
    
    # check the server is actually there
    if not isPortListening(host = host, port = port):
        raise Exception('Could not connect to %s:%d. Is there a server running?' %(host, port))
        
    # build and start broadcaster object
    broadcaster = DataBroadcaster(serverHost = host,
                                  serverPort = port)
    
    # check that there are actually sensors assigned
    if len(broadcaster.rpi.sensors) == 0:
        print 'No sensors registered. Please register some.'
        exit(2)
    
    # run app indefinitely
    broadcaster.run()
    
    try:
        while True:
            # sleep until next poll
            sleep(1)
    except KeyboardInterrupt:
        # react to keyboard interrupt
        pass
    finally:
        # make sure teardown happens for graceful exit
        broadcaster.join()    
    
