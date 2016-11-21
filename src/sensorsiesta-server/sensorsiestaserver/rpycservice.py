from rpyc import Service

from sensorsiestatest.entities import ExampleEntity


class SensorSiestaService(Service):
    
    daoc = None
    dao = None
    
    def on_connect(self):
        if self.dao is None:
            self.dao = self.daoc.daoFor(ExampleEntity)

    def on_disconnect(self):
        pass
    
    def exposed_createByValues(self, **kwargs):
        return self.dao.createByValues(**kwargs)
    
    def exposed_updateByValues(self, uid, **kwargs):
        return self.dao.updateByValues(uid, **kwargs)
    
    def exposed_deleteById(self, uid):
        return self.dao.deleteById(uid)
