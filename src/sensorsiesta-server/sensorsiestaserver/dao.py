#!/usr/bin/python

from sqlite3 import connect
from sensorsiestaserver.entities import ExampleEntity
from sensorsiestaserver.mapping import EntityMapping



class DbConnection(object):
    
    def __init__(self, dbFileName = 'test.db'):
        self.dbFileName = dbFileName
        print 'Connecting to', self.dbFileName
        self.nativeConn = connect(self.dbFileName)
        self.cursor = self.nativeConn.cursor()
    
    def disconnect(self):
        if self.nativeConn:
            print 'Disconnecting from', self.dbFileName
            self.nativeConn.close()
            
    def execSimple(self, query):
        print 'Executing:', query
        self.cursor.execute(query)
    
    def execOneReturn(self, query):
        print 'Executing:', query
        self.cursor.execute(query)
        return self.cursor.fetchone()
    
    def execMultiReturn(self, query):
        print 'Executing:', query
        self.cursor.execute(query)
        return self.cursor.fetchall()



class DAO(object):
    
    def __init__(self, conn, mapping):
        self.conn = conn
        self.mapping = mapping
    
    def findAll(self):
        query = 'SELECT uid, %s FROM %s' %(self.mapping.names(), self.mapping.tableName)
        return [self.mapping.tupleToObj(tup) for tup in self.conn.execMultiReturn(query)]
    
    def findById(self, uid):
        query = 'SELECT uid, %s FROM %s WHERE uid=%d' %(self.mapping.names(), self.mapping.tableName, uid)
        return self.mapping.tupleToObj(self.conn.execOneReturn(query))
    
    def create(self, obj):
        query = 'INSERT INTO %s(%s) VALUES (%s)' %(self.mapping.tableName, self.mapping.names(), self.mapping.values(obj))
        self.conn.execSimple(query)
        obj.uid = self.conn.cursor.lastrowid
        return obj
    
    def createByValues(self, **kwargs):
        return self.create(self.mapping.kwargsToObj(**kwargs))
    
    def update(self, obj):
        query = 'UPDATE %s SET %s WHERE uid=%d' %(self.mapping.tableName, self.mapping.namesWithValues(obj), obj.uid)
        self.conn.execSimple(query)
        
    def updateByValues(self, uid, **kwargs):
        obj = self.mapping.kwargsToObj(**kwargs)
        obj.uid = uid
        return self.update(obj)
    
    def delete(self, obj):
        self.deleteById(obj.uid)
    
    def deleteById(self, uid):
        query = 'DELETE FROM %s WHERE uid=%d' %(self.mapping.tableName, uid)
        self.conn.execSimple(query)
    

        

class DAOContainer(object):
    
    def __init__(self, dbFileName = 'test.db'):
        self.conn = DbConnection(dbFileName)
        self.mappings = {}
        self.daos = {}
    
    
    def mappingFor(self, cls):
        if cls not in self.mappings.keys():
            self.mappings[cls] = EntityMapping(cls)
        return self.mappings[cls]
    
    
    def daoFor(self, cls, recreateTable = False):
        mapping = self.mappingFor(cls)
        cached = mapping.tableName in self.daos.keys()
        
        if recreateTable:
            query = 'DROP TABLE IF EXISTS %s' %(mapping.tableName)
            self.conn.execSimple(query)
        
        if recreateTable or not cached:
            query = 'CREATE TABLE IF NOT EXISTS %s(uid INTEGER PRIMARY KEY AUTOINCREMENT, %s)' %(
                    mapping.tableName, mapping.namesWithSqlType())
            self.conn.execSimple(query)

        if not cached:
            self.daos[mapping.tableName] = DAO(self.conn, mapping)
        
        return self.daos[mapping.tableName]
    
    
    
'''
daoc = DAOContainer()

dao = daoc.daoFor(ExampleEntity, recreateTable = True)

dao.create(ExampleEntity())
dao.createByValues(intMember=84)
dao.create(ExampleEntity(strMember='qwerty'))

print dao.findById(3).__dict__
print [x.__dict__ for x in dao.findAll()]

dao.deleteById(2)
print [x.__dict__ for x in dao.findAll()]

entity = dao.findById(1)
entity.strMember='updated str member'
dao.update(entity)
print dao.findById(1).__dict__

daoc.conn.disconnect()
'''