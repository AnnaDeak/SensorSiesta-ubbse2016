from rpyc import Service

from sensorsiestaserver.entities import ExampleEntity
from sensorsiestaserver.dao import DAOContainer


class SensorSiestaService(Service):
    
    def on_connect(self):
        self.daoc = DAOContainer()
        self.dao = self.daoc.daoFor(ExampleEntity, recreateTable = True)
        self.dao.create(ExampleEntity())
        self.dao.createByValues(intMember=84)
        self.dao.create(ExampleEntity(strMember='qwerty'))

    def on_disconnect(self):
        self.dao = None
        self.daoc.conn.disconnect()
        self.daoc = None
    
    def exposed_createByValues(self, **kwargs):
        return self.dao.createByValues(**kwargs)
    
    def exposed_updateByValues(self, uid, **kwargs):
        return self.dao.updateByValues(uid, **kwargs)
    
    def exposed_deleteById(self, uid):
        return self.dao.deleteById(uid)
