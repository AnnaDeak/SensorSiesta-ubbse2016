import unittest

from sensorsiestaserver.flaskrest import FlaskRestServer
from sensorsiestaserver.entities import ExampleEntity
from sensorsiestaserver.flasksqlalchemy import sqlAlchemyFlask
from sensorsiestacommon.flaskrestclient import FlaskRestClient
from sensorsiestacommon.utils import jsonSerializer
from sensorsiestacommon.entities import Example


class TestSerializeUtils(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        flaskServer = FlaskRestServer(serializer = jsonSerializer)
        flaskServer.wire(ExampleEntity, icls = Example)
        flaskServer.start()
        sqlAlchemyFlask.setApp(flaskServer.flaskApp)
        
        
    def setUp(self):
        self.flaskClient = FlaskRestClient(serializer = jsonSerializer)
        self.e1 = ExampleEntity()
        self.e2 = ExampleEntity(intMember = 84)
        self.e3 = ExampleEntity(strMember = 'qwerty')
        
        sqlAlchemyFlask.drop_all()
        sqlAlchemyFlask.create_all()
        session = sqlAlchemyFlask.session
        session.add(self.e1)
        session.add(self.e2)
        session.add(self.e3)
        session.commit()
        
    
    
    def testFindAll(self):
        result = self.flaskClient.request('Examples')
        self.assertSame(result['Examples'][0], self.e1)
        self.assertSame(result['Examples'][1], self.e2)
        self.assertSame(result['Examples'][2], self.e3)
        
        
    def testFindById(self):
        result = self.flaskClient.request('Examples/1')
        self.assertSame(result['Example'], self.e1)
        result = self.flaskClient.request('Examples/2')
        self.assertSame(result['Example'], self.e2)
        result = self.flaskClient.request('Examples/3')
        self.assertSame(result['Example'], self.e3)
    
    
    def testCreate(self):
        newE = ExampleEntity(intMember = 55)
        self.flaskClient.request('Examples', method = 'POST', intMember = 55)
        result = self.flaskClient.request('Examples/4')
        self.assertSame(result['Example'], newE)
    
    
    def testDelete(self):
        self.flaskClient.request('Examples/2', method = 'DELETE')
        result = self.flaskClient.request('Examples')
        self.assertSame(result['Examples'][0], self.e1)
        self.assertSame(result['Examples'][1], self.e3)
        
        
    def testUpdate(self):
        self.e1.strMember = 'updatedStrMember'
        self.flaskClient.request('Examples/1', method = 'PUT', strMember = 'updatedStrMember')
        result = self.flaskClient.request('Examples/1')
        self.assertSame(result['Example'], self.e1)
        
        
    def assertSame(self, a, b):
        self.assertIsInstance(a, Example)
        self.assertEquals(a.intMember, b.intMember)
        self.assertEquals(a.floatMember, b.floatMember)
        #self.assertEquals(a.dateMember, b.dateMember)
        self.assertEquals(a.strMember, b.strMember)
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
