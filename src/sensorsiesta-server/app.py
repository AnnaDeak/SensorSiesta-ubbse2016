from getopt import getopt, GetoptError
from sys import argv
from os import getenv

from sensorsiestaserver.flaskrest import FlaskRestServer
from sensorsiestacommon.entities import SensorReading, Sensor, SensorType, RPi
from sensorsiestacommon.utils import jsonSerializerWithUri
from sensorsiestacommon.flasksqlalchemy import sqlAlchemyFlask


def printHelp():
    print '''SensorSiesta Server
-------------------

Arguments:
    -h             Print current help information
    -d, --db       Path to sqlite database file (use :memory: for in-memory db)
    -p, --port     Specify port to listen on (by default, env var PORT or 5000)
    -v, --verbose  Give verbose database query output.
    '''
    
    

if __name__ == '__main__':
    
    # default settings
    dbName = 'test.db'
    port = getenv('PORT', 5000)
    verbose = False
    
    # parse command-line arguments
    try:
        opts, args = getopt(argv[1:], "hd:p:v", ["db=", "port=", "verbose"])
    except GetoptError:
        printHelp()
        exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            printHelp()
            exit()
        elif opt in ("-s", "--db"):
            dbName = arg
        elif opt in ("-p", "--port"):
            port = int(arg)
        elif opt in ("-v", "--verbose"):
            verbose = True
    
    
    # set up flask server
    flaskServer = FlaskRestServer(dbUri = 'sqlite:///' + dbName,
                                  port = port,
                                  verbose = verbose,
                                  serializer = jsonSerializerWithUri)
    
    # wire entities
    flaskServer.wire(SensorReading)
    flaskServer.wire(Sensor)
    flaskServer.wire(SensorType)
    flaskServer.wire(RPi)
    flaskServer.wireOneToMany(RPi, Sensor, 'sensors')
    flaskServer.wireOneToMany(SensorType, Sensor, 'sensors')
    flaskServer.wireOneToMany(Sensor, SensorReading, 'readings')
    
    
    # set up flask-sqlalchemy & create tables
    sqlAlchemyFlask.setApp(flaskServer.flaskApp)
    sqlAlchemyFlask.create_all()
    
    # start flask server on local thread
    flaskServer.start(threaded = False)
    
