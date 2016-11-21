from datetime import datetime
from sensorsiestaserver.utils import timeToSeconds, secondsToTime


class PropertyMapping(object):
    def __init__(self, name):
        self.name = name
    
    def to(self, localProp):
        return str(localProp)
    
    def fr(self, sqlProp):
        return sqlProp
    
    
class IntPropertyMapping(PropertyMapping):
    
    localType = int
    sqlType = 'INTEGER'
    

class FloatPropertyMapping(PropertyMapping):
    
    localType = float
    sqlType = 'REAL'
    

class StringPropertyMapping(PropertyMapping):
    
    localType = str
    sqlType = 'TEXT'
    
    def to(self, localProp):
        return "'%s'" %(localProp)
    

class DatePropertyMapping(PropertyMapping):
    
    localType = datetime
    sqlType = 'INTEGER'
    
    def __init__(self, name):
        self.name = name
    
    def to(self, localProp):
        return str(timeToSeconds(localProp))
    
    def fr(self, sqlProp):
        return secondsToTime(sqlProp)
        


class PropertyMappingContainer(object):
    
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
    
    def __init__(self, obj):
        self.objType = type(obj)
        self.tableName = self.objType.__name__
        
        self.props = {}
        
        for propName, propValue in obj.__dict__.iteritems():
            if propName is not 'uid':
                mapperClass = PropertyMappingContainer.mappingFor(propValue)
                self.props[propName] = mapperClass(propName)
    
    def names(self):
        return ', '.join(self.props.keys())
    
    def namesWithSqlType(self):
        return ', '.join(['%s %s' %(name, mapping.sqlType) for name, mapping in self.props.iteritems()])
    
    def values(self, obj):
        return ', '.join([mapping.to(obj.__dict__[name]) for name, mapping in self.props.iteritems()])
    
    def namesWithValues(self, obj):
        return ', '.join(['%s=%s' %(name, mapping.to(obj.__dict__[name])) for name, mapping in self.props.iteritems()])

    def tupleToObj(self, tup):
        ret = self.objType()
        ret.uid = tup[0]
        for i in range(len(self.props)):
            ret.__dict__[self.props.keys()[i]] = self.props.values()[i].fr(tup[i+1])
        return ret
    
    