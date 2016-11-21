from rpyc.utils.server import ThreadedServer

from sensorsiestaserver.dao import DAOContainer
from sensorsiestaserver.service import SensorSiestaService


if __name__ == '__main__':
    
    print 'Starting remote DAO service'
    ThreadedServer(SensorSiestaService, port = 8000).start()
