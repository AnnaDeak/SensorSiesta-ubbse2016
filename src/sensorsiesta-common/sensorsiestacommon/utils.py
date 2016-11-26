'''
Utilities
@author Csaba Sulyok
'''

from datetime import datetime
import json
from pytz import utc
from socket import socket, AF_INET, SOCK_STREAM
from sqlalchemy.sql.type_api import TypeDecorator
from sqlalchemy.sql.sqltypes import DateTime


'''
Serialization
'''

class JsonSerializer(object):
    '''
    JSON serializer.
    '''
    
    contentType='application/json'
    currentUri = None
    
    
    def toDict(self, obj, preserveClassData = True):
        '''
        Create dict from arbitrary object.
        If a class instance is found, it is dictified together with its module & class name.
        '''
        if isinstance(obj, list):
            ret = obj[:]
            # recurse through list members to dictify children
            for idx, value in enumerate(ret):
                ret[idx] = self.toDict(value, preserveClassData)
        elif isinstance(obj, dict):
            ret = { key: value for key, value in obj.iteritems() if not key.startswith('_') }
            # recurse through dict members to dictify children
            for name, value in ret.iteritems():
                ret[name] = self.toDict(value, preserveClassData)
        elif hasattr(obj, '__dict__'):
            # if class instance, save class name in dict
            ret = { key: value for key, value in obj.__dict__.iteritems() if not key.startswith('_') }
            # recurse through dict members to dictify children which are class instances
            for name, value in ret.iteritems():
                ret[name] = self.toDict(value, preserveClassData)
            # code in class data to json if needed
            if preserveClassData:
                ret['__moduleName__'] = obj.__module__
                ret['__className__'] = obj.__class__.__name__
        elif isinstance(obj, datetime):
            ret = timeToSeconds(obj)
        else:
            ret = obj
            
        return ret
        
        
    def fromDict(self, objDict, checkForClassData = True):
        '''
        Inverse of toDict, takes a dict and finds members with module & class names,
        and builds their instances.
        '''
        if isinstance(objDict, list):
            ret = objDict[:]
            # recurse through list members to de-dictify children
            for idx, value in enumerate(ret):
                ret[idx] = self.fromDict(value, checkForClassData)
        elif isinstance(objDict, dict):
            ret = objDict.copy()
            
            # iterate through children first
            for name, value in ret.iteritems():
                ret[name] = self.fromDict(value, checkForClassData)
            
            # check if class & module name given, otherwise it's just an actual dict
            if checkForClassData and '__className__' in ret:
                # find module & class declared in dict, and load it
                module = __import__(ret['__moduleName__'], globals(), locals(), ret['__className__'])
                clazz = getattr(module, ret['__className__'])
                
                # remove extra fields from dict and call constructor using what remains
                del ret['__moduleName__']
                del ret['__className__']
                
                obj = clazz()
                for name, value in ret.iteritems():
                    if hasattr(obj, name):
                        setattr(obj, name, value)
                    else:
                        raise Exception('Cannot deserialize: %s has no member %s' %(clazz, name))
                ret = obj
        elif isinstance(objDict, int) and objDict > 100000000:
            # ugly assumption for date here
            ret = secondsToTime(objDict)
        else:
            ret = objDict
        
        return ret

    def _to(self, obj):
        return json.dumps(self.toDict(obj))
    
    def _from(self, objStr):
        return self.fromDict(json.loads(objStr))
    
    
        

class JsonSerializerWithUris(JsonSerializer):
    '''
    Extended JSON serializer.
    Also appends URIs.
    '''
    
    def _decorateWithUris(self, objDict, uri):
        '''
        Parse dict recursively and add uri to each member.
        '''
        if isinstance(objDict, list):
            for idx, value in enumerate(objDict):
                uriIdx = value['uid'] if 'uid' in value else idx
                subUri = '%s/%d' %(uri, uriIdx)
                self._decorateWithUris(value, subUri)
        elif isinstance(objDict, dict):
            innerListNames = []
            for name, value in objDict.iteritems():
                if isinstance(value, list):
                    innerListNames.append(name)
                subUri = '%s/%s' %(uri, name)
                self._decorateWithUris(value, subUri)
            objDict['uri'] = uri
            for name in innerListNames:
                objDict[name + '_uri'] = subUri = '%s/%s' %(uri, name)
    
    
    def _removeUris(self, objDict):
        '''
        Remove URI fields from dict so it can then be properly
        deserialized.
        '''
        if isinstance(objDict, list):
            for _, value in enumerate(objDict):
                self._removeUris(value)
        elif isinstance(objDict, dict):
            if 'uri' in objDict:
                del objDict['uri']
            for _, value in objDict.iteritems():
                self._removeUris(value)
            
            
    def _to(self, obj):
        '''
        Serialize to JSON, but before serializing converted dict,
        add URIs to each field.
        '''
        objDict = self.toDict(obj, preserveClassData = True)
        if self.currentUri != None:
            for _, value in objDict.iteritems():
                self._decorateWithUris(value, self.currentUri)
        return json.dumps(objDict)
    
    
    def _from(self, jsonStr):
        '''
        Deserialize JSON, ommitting all URI values.
        '''
        objDict = json.loads(jsonStr)
        self._removeUris(objDict)
        return self.fromDict(objDict, checkForClassData = True)
    
    
'''
Define basic serializers which can be used in web services.
'''
jsonSerializer = JsonSerializer()
jsonSerializerWithUri = JsonSerializerWithUris()



'''
Datetime utilities
'''

epochDateTime = datetime(1970, 1, 1).replace(tzinfo=utc)
defaultFormat = '%Y-%m-%d %H:%M:%S.%f'


class TimeZoneAwareDateTime(TypeDecorator):
    '''
    Results returned as aware datetimes, not naive ones.
    '''

    impl = DateTime

    def process_result_value(self, value, dialect):
        return value.replace(tzinfo=utc)
    
    

def timeToSeconds(givenDateTime):
    '''
    Converts datetime to total number of seconds.
    '''
    timeDiff = givenDateTime - epochDateTime
    return int(timeDiff.total_seconds())


def secondsToTime(seconds):
    '''
    Converts number of seconds since epoch to formatted datetime
    in the Drive API format.
    '''
    return datetime.fromtimestamp(seconds, utc)


'''
Socket Utils
'''
def isPortListening(host='127.0.0.1', port=5000):
    '''
    Attempts a socket call to a host:port
    and returns if that host:port is listening.
    '''
    sock = socket(AF_INET, SOCK_STREAM)
    result = sock.connect_ex((host, port))
    return result == 0