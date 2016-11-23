'''
Test rest calls through http using these methods
'''

import socket
from traceback import print_exc
from httplib import HTTPConnection

from sensorsiestacommon.utils import jsonSerializerWithUri


class FlaskRestClient(object):
	
	def __init__(self, host = 'localhost',
				       port = 5000,
				       serializer = jsonSerializerWithUri):
		self.host = host
		self.port = port
		self.serializer = serializer
		
		self.conn = HTTPConnection(host = self.host, port = self.port)
	
	
	def request(self, urlname = '/',
					  method = 'GET',
			          **kwargs):
		'''
		Send an HTTP request,
		then try to deserialize response and return it.
		'''
		try:
			self.conn.request(method, 
							  urlname,
							  body = self.serializer._to(kwargs),
							  headers={'Content-Type': self.serializer.contentType})
		except socket.error:
			raise Exception('Could not connect to %s:%d. Is there a server running?' %(self.host, self.port))
		except Exception, e:
			try:
				errorMsg = e.read()
				remoteException = self.serializer._from(errorMsg)
			except Exception, e2:
				remoteException = '%s Could not deserialize %s: %s' %(e.msg, errorMsg, e2)
			raise Exception('Remote exception code %d: %s' %(e.code, remoteException))
		
		response = self.conn.getresponse()
		responseContent = response.read()
		
		try:
			ret = self.serializer._from(responseContent)
		except:
			print_exc()
			raise Exception('Could not deserialize received data using method %s: %s' %(
							self.serializer._from.__name__, responseContent))
		if isinstance(ret, Exception):
			raise ret
		return ret 
		