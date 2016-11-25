import unittest

from sensorsiestaserver.flaskrest import FlaskRestServer
from sensorsiestacommon.entities import ExampleEntity
from sensorsiestacommon.flaskrestclient import FlaskRestClient
from sensorsiestacommon.utils import jsonSerializer
from sensorsiestacommon.flasksqlalchemy import sqlAlchemyFlask


class TestSerializeUtils(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        flaskServer = FlaskRestServer(serializer = jsonSerializer)
        flaskServer.wire(ExampleEntity)
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
        result = self.flaskClient.request('ExampleEntitys')
        self.assertSame(result['ExampleEntitys'][0], self.e1)
        self.assertSame(result['ExampleEntitys'][1], self.e2)
        self.assertSame(result['ExampleEntitys'][2], self.e3)
        
        
    def testFindById(self):
        result = self.flaskClient.request('ExampleEntitys/1')
        self.assertSame(result['ExampleEntity'], self.e1)
        result = self.flaskClient.request('ExampleEntitys/2')
        self.assertSame(result['ExampleEntity'], self.e2)
        result = self.flaskClient.request('ExampleEntitys/3')
        self.assertSame(result['ExampleEntity'], self.e3)
    
    
    def testCreate(self):
        newE = ExampleEntity(intMember = 55)
        self.flaskClient.request('ExampleEntitys', method = 'POST', intMember = 55)
        result = self.flaskClient.request('ExampleEntitys/4')
        self.assertSame(result['ExampleEntity'], newE)
    
    
    def testDelete(self):
        self.flaskClient.request('ExampleEntitys/2', method = 'DELETE')
        result = self.flaskClient.request('ExampleEntitys')
        self.assertSame(result['ExampleEntitys'][0], self.e1)
        self.assertSame(result['ExampleEntitys'][1], self.e3)
        
        
    def testUpdate(self):
        self.e1.strMember = 'updatedStrMember'
        self.flaskClient.request('ExampleEntitys/1', method = 'PUT', strMember = 'updatedStrMember')
        result = self.flaskClient.request('ExampleEntitys/1')
        self.assertSame(result['ExampleEntity'], self.e1)
        
        
    def assertSame(self, a, b):
        self.assertIsInstance(a, ExampleEntity)
        self.assertEquals(a.intMember, b.intMember)
        self.assertEquals(a.floatMember, b.floatMember)
        #self.assertEquals(a.dateMember, b.dateMember)
        self.assertEquals(a.strMember, b.strMember)
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
