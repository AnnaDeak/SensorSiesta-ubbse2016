from threading import Thread

from rpyc.utils.server import ThreadedServer

from sensorsiestaserver.dao import DAOContainer
from sensorsiestaserver.service import SensorSiestaService
from sensorsiestaserver.flaskrest import wire, expose
from sensorsiestatest.entities import ExampleEntity
from sensorsiestaserver.utils import jsonSerializerWithUri


if __name__ == '__main__':
    
    daoc = DAOContainer()
    
    SensorSiestaService.daoc = daoc
    rpycServer = ThreadedServer(SensorSiestaService, port = 8000)
    print 'Starting remote DAO service'
    rpycThread = Thread(target = rpycServer.start)
    rpycThread.start()
        
    dao = daoc.daoFor(ExampleEntity, recreateTable = True)
    dao.create(ExampleEntity())
    dao.createByValues(intMember=84)
    dao.create(ExampleEntity(strMember='qwerty'))
        
    wire('example', dao, serializer=jsonSerializerWithUri)
    expose(threaded = False)
