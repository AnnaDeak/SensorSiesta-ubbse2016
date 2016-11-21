'''
General database connectivity layer using sqlite3.
@author Csaba Sulyok
'''

from sqlite3 import connect
from sensorsiestaserver.mapping import EntityMapping



class DbConnection(object):
    '''
    Wrapper around general sqlite3 database connection.
    '''
    
    def __init__(self, dbFileName = 'test.db'):
        '''
        Initialize using file name or :memory:
        '''
        self.dbFileName = dbFileName
        print 'Connecting to', self.dbFileName
        self.nativeConn = connect(self.dbFileName, check_same_thread=False)
        self.cursor = self.nativeConn.cursor()
    
    
    def disconnect(self):
        '''
        Break connection.
        '''
        if self.nativeConn:
            print 'Disconnecting from', self.dbFileName
            self.nativeConn.close()
            
            
    def execSimple(self, query):
        '''
        Execute SQL query with no expected return value.
        '''
        print 'Executing:', query
        self.cursor.execute(query)
    
    
    def execOneReturn(self, query):
        '''
        Execute SQL query with a one row expected return value.
        '''
        print 'Executing:', query
        self.cursor.execute(query)
        return self.cursor.fetchone()
    
    
    def execMultiReturn(self, query):
        '''
        Execute SQL query with multiple rows in the expected return value.
        '''
        print 'Executing:', query
        self.cursor.execute(query)
        return self.cursor.fetchall()



class DAO(object):
    '''
    Data access object for a general entity.
    '''
    
    def __init__(self, conn, mapping):
        '''
        Initialize using DbConnection and EntityMapping.
        '''
        self.conn = conn
        self.mapping = mapping
    
    
    def findAll(self):
        '''
        Find all rows for an entity in sqlite table.
        Performs casting over to object list.
        '''
        query = 'SELECT uid, %s FROM %s' %(self.mapping.names(), self.mapping.tableName)
        return [self.mapping.tupleToObj(tup) for tup in self.conn.execMultiReturn(query)]
    
    
    def findById(self, uid):
        '''
        Find row by ID in sqlite table.
        Performs casting over to object.
        '''
        query = 'SELECT uid, %s FROM %s WHERE uid=%d' %(self.mapping.names(), self.mapping.tableName, uid)
        return self.mapping.tupleToObj(self.conn.execOneReturn(query))
    
    
    def create(self, obj):
        '''
        Insert row into sqlite table.
        UID associated dynamically.
        @return Newly built entity with UID set.
        '''
        query = 'INSERT INTO %s(%s) VALUES (%s)' %(self.mapping.tableName, self.mapping.names(), self.mapping.values(obj))
        self.conn.execSimple(query)
        obj.uid = self.conn.cursor.lastrowid
        print 'New row ID', obj.uid
        return obj
    
    
    def createByValues(self, **kwargs):
        '''
        Insert row based on arguments, not object.
        UID associated dynamically.
        @return Newly built entity with UID set.
        '''
        return self.create(self.mapping.kwargsToObj(**kwargs))
    
    
    def update(self, obj):
        '''
        Update row based on object.
        @return Updated entity.
        '''
        query = 'UPDATE %s SET %s WHERE uid=%d' %(self.mapping.tableName, self.mapping.namesWithValues(obj), obj.uid)
        self.conn.execSimple(query)
        return obj

        
    def updateByValues(self, uid, **kwargs):
        '''
        Update row based on arguments, not object.
        @return Updated entity.
        '''
        obj = self.mapping.kwargsToObj(**kwargs)
        obj.uid = uid
        return self.update(obj)
    
    
    def deleteById(self, uid):
        '''
        Delete row from table using UID.
        '''
        query = 'DELETE FROM %s WHERE uid=%d' %(self.mapping.tableName, uid)
        self.conn.execSimple(query)
    
    
    def deleteAll(self):
        '''
        Deletes all rows from table.
        '''
        query = 'DELETE FROM %s' %(self.mapping.tableName)
        self.conn.execSimple(query)
    


class DAOContainer(object):
    '''
    Cache/factory for DAOs and entity mappings.
    Using a single connection, one can cache multiple DAOs so
    that the same instance may be recalled if used from multiple places.
    '''
    
    def __init__(self, dbFileName = 'test.db'):
        self.conn = DbConnection(dbFileName)
        self.mappings = {}
        self.daos = {}
    
    
    def mappingFor(self, cls):
        '''
        Retrieve entity mapping for a given class.
        Uses cache pattern.
        '''
        if cls not in self.mappings.keys():
            self.mappings[cls] = EntityMapping(cls)
        return self.mappings[cls]
    
    
    def recreateTable(self, cls):
        '''
        Drops and recreates table associated with class.
        Besides clearing all data, also makes sure schema is up-to-date.
        '''
        mapping = self.mappingFor(cls)
        query = 'DROP TABLE IF EXISTS %s' %(mapping.tableName)
        self.conn.execSimple(query)
        query = 'CREATE TABLE IF NOT EXISTS %s(uid INTEGER PRIMARY KEY AUTOINCREMENT, %s)' %(
                mapping.tableName, mapping.namesWithSqlType())
        self.conn.execSimple(query)
    
    
    def daoFor(self, cls, recreateTable = False):
        '''
        Retrieve DAO for a given entity class.
        Uses cache pattern.
        Takes care that the table exists in the sqlite DB.
        '''
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