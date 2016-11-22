from threading import Thread

from rpyc.utils.server import ThreadedServer

from sensorsiestaserver.dao import DAOContainer
from sensorsiestaserver.rpycservice import SensorSiestaService
from sensorsiestaserver.flaskrest import FlaskRestServer
from sensorsiestatest.entities import ExampleEntity
from sensorsiestaserver.utils import jsonSerializerWithUri


if __name__ == '__main__':
    
    rpycPort = 8000
    flaskPort = 5000
    
    # build dao container - establish connection to db
    daoContainer = DAOContainer()
    
    # set up rpyc server
    SensorSiestaService.daoContainer = daoContainer
    rpycServer = ThreadedServer(SensorSiestaService,
                                port = rpycPort,
                                protocol_config = {"allow_all_attrs" : True})
    # start rpyc listener on different thread
    print 'Starting remote DAO service'
    rpycThread = Thread(target = rpycServer.start)
    rpycThread.start()

    # set up flask server
    flaskServer = FlaskRestServer(daoContainer = daoContainer,
                                  port = flaskPort,
                                  serializer = jsonSerializerWithUri)
    flaskServer.wire(ExampleEntity)
    # start flask server on local thread
    flaskServer.start(threaded = False)
    
