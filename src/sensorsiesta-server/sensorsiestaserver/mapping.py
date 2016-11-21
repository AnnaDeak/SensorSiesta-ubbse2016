'''
Entity mappings between Python and sqlite.
Enables pairing of properties and entities with custom converters.
@author Csaba Sulyok
'''

from datetime import datetime
from sensorsiestaserver.utils import timeToSeconds, secondsToTime


class PropertyMapping(object):
    '''
    General property mapping.
    Conversion only done through toString-ing.
    '''
    def __init__(self, name):
        self.name = name
    
    def to(self, localProp):
        return str(localProp)
    
    def fr(self, sqlProp):
        return sqlProp
    
    
class IntPropertyMapping(PropertyMapping):
    '''
    Custom property mapping with parallel sqlite type.
    '''
    localType = int
    sqlType = 'INTEGER'
    

class FloatPropertyMapping(PropertyMapping):
    '''
    Custom property mapping with parallel sqlite type.
    '''
    localType = float
    sqlType = 'REAL'
    

class StringPropertyMapping(PropertyMapping):
    '''
    Custom property mapping with parallel sqlite type.
    '''
    localType = str
    sqlType = 'TEXT'
    
    def to(self, localProp):
        '''
        Strings given quotemarks to comply with SQL standards.
        '''
        return "'%s'" %(localProp)
    

class DatePropertyMapping(PropertyMapping):
    '''
    Custom property mapping for date.
    We save it as number of seconds since epoch.
    '''
    
    localType = datetime
    sqlType = 'INTEGER'
    
    def __init__(self, name):
        self.name = name
    
    def to(self, localProp):
        return str(timeToSeconds(localProp))
    
    def fr(self, sqlProp):
        return secondsToTime(sqlProp)
        


class PropertyMappingContainer(object):
    '''
    Static container of property mappings.
    '''
    propertyMappings = {
                        int : IntPropertyMapping,
                        float : FloatPropertyMapping,
                        str : StringPropertyMapping,
                        datetime : DatePropertyMapping
                        }
    
    @staticmethod
    def mappingFor(obj):
        if type(obj) in PropertyMappingContainer.propertyMappings:
            return PropertyMappingContainer.propertyMappings[type(obj)]
        else:
            raise Exception('Type not mapped: %s' %(type(obj)))



class EntityMapping(object):
    '''
    Mapping of an entity to an sqlite table.
    Contains map of properties and helper methods for SQL string formatting.
    '''
    
    def __init__(self, cls):
        self.cls = cls
        obj = cls()
        self.tableName = self.cls.__name__
        
        self.props = {}
        
        for propName, propValue in obj.__dict__.iteritems():
            if propName is not 'uid':
                mapperClass = PropertyMappingContainer.mappingFor(propValue)
                self.props[propName] = mapperClass(propName)
    
    
    #===============================
    # HELPER METHODS FOR SQL QUERYS
    #===============================
    
    
    def names(self):
        '''
        Property names separated by commas.
        '''
        return ', '.join(self.props.keys())
    
    
    def namesWithSqlType(self):
        '''
        Property names together with sqlite types.
        '''
        return ', '.join(['%s %s' %(name, mapping.sqlType) for name, mapping in self.props.iteritems()])
    
    
    def values(self, obj):
        '''
        Values from an entity separated by commas.
        Ensures same order as names().
        '''
        return ', '.join([mapping.to(obj.__dict__[name]) for name, mapping in self.props.iteritems()])
    
    
    def namesWithValues(self, obj):
        '''
        Property names and value from an entity, separated by commas.
        Used for update calls.
        '''
        return ', '.join(['%s=%s' %(name, mapping.to(obj.__dict__[name])) for name, mapping in self.props.iteritems()])


    def tupleToObj(self, tup):
        '''
        Build entity object by tuple (standard return type of sqlite).
        '''
        ret = self.cls()
        ret.uid = tup[0]
        for i in range(len(self.props)):
            ret.__dict__[self.props.keys()[i]] = self.props.values()[i].fr(tup[i+1])
        return ret
    
    
    def kwargsToObj(self, **kwargs):
        '''
        Build entity object by arguments.
        '''
        ret = self.cls()
        for propName, propValue in kwargs.iteritems():
            ret.__dict__[propName] = propValue
        return ret
    
