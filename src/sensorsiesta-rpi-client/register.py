'''
Register sensors to server.
@author Csaba Sulyok
'''

from sys import argv
from getopt import GetoptError, getopt

from sensorsiestaclient.acquire import acquireRPi
from sensorsiestacommon.utils import isPortListening
from sensorsiestacommon.flaskrestclient import FlaskRestClient


def printHelp():
    print '''
SensorSiesta: Register pins on current machine to server
--------------------------------------------------------
Usage:
    python register.py -n <pinNumber> [-i <interval> -s <serverHost> -p <serverPort>]
    python register.py -c [-s <serverHost> -p <serverPort>]
    
Arguments:
    -h, --help     Print current help information
    -s, --host     Specify host of SensorSiesta server (by default, localhost)
    -p, --port     Specify port of SensorSiesta server (by default, 5000)
    -c, --clear    Delete all sensors associated with device on server.
    -p, --pin      Pin number to listen to.
    -i, --interval Poll interval of sensor
    '''
    
    
if __name__ == '__main__':
    
    # default settings
    host = 'localhost'
    port = 5000
    clear = False
    pin = -1
    interval = 2.0
    
    # parse command-line arguments
    try:
        opts, args = getopt(argv[1:], 'hs:p:cn:i:', ['help', 'host=', 'port=', 'clear', 'pin=', 'interval='])
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
        elif opt in ('-c', '--clear'):
            clear = True
        elif opt in ('-n', '--pin'):
            pin = int(arg)
        elif opt in ('-i', '--interval'):
            interval = float(arg)
            
    
    # check the server is actually there
    if not isPortListening(host = host, port = port):
        raise Exception('Could not connect to %s:%d. Is there a server running?' %(host, port))
    
    # build connection to server    
    conn = FlaskRestClient(host = host, port = port)
    
    # if asked to delete
    if clear:
        rpi = acquireRPi(conn, create = False)
        if rpi is not None:
            print 'Clearing current device'
            conn.request('/RPis/%d' %(rpi.uid), method = 'DELETE')
            
    else:
        if pin == -1:
            printHelp()
            exit(2)
        else:
            # acquire and create if not exists
            rpi = acquireRPi(conn)
            print 'Adding sensor:', pin, interval
            conn.request('/Sensors', method = 'POST',
                         sensorTypeUid = 1, rpiUid = rpi.uid,
                         pinNumber = pin, pollInterval = interval)
            