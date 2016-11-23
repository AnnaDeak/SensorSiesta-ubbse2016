from sensorsiestaserver.dao import DAOContainer
from sensorsiestaserver.flaskrest import FlaskRestServer
from sensorsiestacommon.entities import ExampleEntity
from sensorsiestacommon.utils import jsonSerializerWithUri


if __name__ == '__main__':
    
    port = 5000
    
    # build dao container - establish connection to db
    daoContainer = DAOContainer()
    
    # set up flask server
    flaskServer = FlaskRestServer(daoContainer = daoContainer,
                                  port = port,
                                  serializer = jsonSerializerWithUri)
    flaskServer.wire(ExampleEntity)
    # start flask server on local thread
    flaskServer.start(threaded = False)
    
