import unittest

from sensorsiestaserver.dao import DAOContainer
from sensorsiestaserver.flaskrest import wire, expose
from sensorsiestatest.entities import ExampleEntity
from sensorsiestatest.flaskrestclient import request


class TestSerializeUtils(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.daoc = DAOContainer()
        self.dao = self.daoc.daoFor(ExampleEntity, recreateTable = True)
        wire('example', self.dao)
        expose()
        
        
    def setUp(self):
        self.e1 = ExampleEntity()
        self.e2 = ExampleEntity(intMember = 84)
        self.e3 = ExampleEntity(strMember = 'qwerty')
        
        self.daoc.recreateTable(ExampleEntity)
        self.dao.create(self.e1)
        self.dao.create(self.e2)
        self.dao.create(self.e3)
        
    
    
    def testFindAll(self):
        result = request('example')
        self.assertSame(result[0], self.e1)
        self.assertSame(result[1], self.e2)
        self.assertSame(result[2], self.e3)
        
        
    def testFindById(self):
        result = request('example/1')
        self.assertSame(result, self.e1)
        result = request('example/2')
        self.assertSame(result, self.e2)
        result = request('example/3')
        self.assertSame(result, self.e3)
    
    
    def testCreate(self):
        newE = ExampleEntity(intMember = 55)
        request('example', method = 'POST', intMember = 55)
        result = request('example/4')
        self.assertSame(result, newE)
    
    
    def testDelete(self):
        request('example/2', method = 'DELETE')
        result = request('example')
        self.assertSame(result[0], self.e1)
        self.assertSame(result[1], self.e3)
        
        
    def testUpdate(self):
        self.e1.strMember = 'updatedStrMember'
        request('example/1', method = 'PUT', strMember = 'updatedStrMember')
        result = request('example/1')
        self.assertSame(result, self.e1)
        
        
    def assertSame(self, a, b):
        self.assertEquals(a.intMember, b.intMember)
        self.assertEquals(a.floatMember, b.floatMember)
        #self.assertEquals(a.dateMember, b.dateMember)
        self.assertEquals(a.strMember, b.strMember)
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
