from rpyc import Service

from sensorsiestacommon.entities import ExampleEntity


class SensorSiestaService(Service):
    
    daoContainer = None
    dao = None
    
    def on_connect(self):
        if self.dao is None:
            self.dao = self.daoContainer.daoFor(ExampleEntity)

    def on_disconnect(self):
        pass
    
    def exposed_createByValues(self, **kwargs):
        return self.dao.createByValues(**kwargs)
    
    def exposed_updateByValues(self, uid, **kwargs):
        return self.dao.updateByValues(uid, **kwargs)
    
    def exposed_deleteById(self, uid):
        return self.dao.deleteById(uid)
