'''
Acquire RPi and Sensor info for current machine
from server
'''
import socket


def acquireRPi(conn, create = True, sensors = True):
    '''
    Find current device on server based on host name.
    If it doesn't exist and create is set, it gets created.
    '''
    rpi = None
    host = socket.gethostname()
    
    print 'Check if current host registered:', host
    response = conn.request(urlname = '/RPis?host=%s' %(host))
    
    if len(response['RPis']) > 0:
        rpi = response['RPis'][0]
        print 'Found on server, uid = %d' %(rpi.uid)
        if sensors:
            print 'Retrieving sensors'
            subresponse = conn.request(urlname = '/Sensors?rpiUid=%d' %(rpi.uid))
            rpi.sensors = subresponse['Sensors']
            
    elif create:
        print 'Not found on server, creating'
        response = conn.request(urlname = '/RPis',
                                method = 'POST',
                                host = host)
        rpi = response['RPi']
        print 'Assigned uid = %d' %(rpi.uid)
    else:
        print 'Not found on server, not creating'
    
    return rpi
