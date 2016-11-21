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
    
    def update(self, obj):
        query = 'UPDATE %s SET %s WHERE uid=%d' %(self.mapping.tableName, self.mapping.namesWithValues(obj), obj.uid)
        self.conn.execSimple(query)
    
    def delete(self, obj):
        self.deleteById(obj.uid)
    
    def deleteById(self, uid):
        query = 'DELETE FROM %s WHERE uid=%d' %(self.mapping.tableName, uid)
        self.conn.execSimple(query)
    

        

class TableManager(object):
    
    def __init__(self, conn):
        self.conn = conn
    
    
    def createTable(self, mapping, drop = False):
        if drop:
            self.dropTable(tableName = mapping.tableName)
            
        query = 'CREATE TABLE IF NOT EXISTS %s(uid INTEGER PRIMARY KEY AUTOINCREMENT, %s)' %(
                mapping.tableName, mapping.namesWithSqlType())
        
        self.conn.execSimple(query)
        return DAO(conn, mapping)
    
    
    def dropTable(self, obj = None, tableName = None):
        if tableName is None:
            if obj is not None:
                tableName = type(obj).__name__
            else:
                print 'No table name to drop'
                return
        
        query = 'DROP TABLE IF EXISTS %s' %tableName
        self.conn.execSimple(query)
    
    
    

conn = DbConnection()
tm = TableManager(conn)
mapping = EntityMapping(ExampleEntity())

dao = tm.createTable(mapping, drop = True)

dao.create(ExampleEntity())
dao.create(ExampleEntity(intMember=84))
dao.create(ExampleEntity(strMember='qwerty'))

print dao.findById(3).__dict__
print [x.__dict__ for x in dao.findAll()]

dao.deleteById(2)
print [x.__dict__ for x in dao.findAll()]

entity = dao.findById(1)
entity.strMember='updated str member'
dao.update(entity)
print dao.findById(1).__dict__

conn.disconnect()