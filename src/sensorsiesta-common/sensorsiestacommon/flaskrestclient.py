'''
Test rest calls through http using these methods
'''

from urllib2 import urlopen, Request, HTTPError, URLError

from traceback import print_exc
from sensorsiestaserver.utils import jsonSerializer


def request(urlname = None,
			host = '127.0.0.1', port = 5000,
			method = 'GET',
			url = None,
			serializer = jsonSerializer,
			**kwargs):
	'''
	Send an HTTP request,
	then try to deserialize response and return it.
	'''
	
	if url is None:
		url = 'http://%s:%s/%s' %(host, port, urlname)
	request = RequestWithMethod(url = url, method = method, data = serializer._to(kwargs), 
					            headers={'Content-Type': serializer.contentType})

	try:
		#print 'Sending %s to %s' %(request._method, request._url)
		connection = urlopen(request)
	except HTTPError, e:
		try:
			errorMsg = e.read()
			remoteException = serializer._from(errorMsg)
		except Exception, e2:
			remoteException = '%s Could not deserialize %s: %s' %(e.msg, errorMsg, e2)
		raise Exception('Remote exception code %d: %s' %(e.code, remoteException))
	except URLError, e:
		raise Exception('Could not connect to %s. Is there a server running?' %(request.host))
		
	content = connection.read()
	try:
		ret = serializer._from(content)
	except:
		print_exc()
		raise Exception('Could not deserialize received data using method %s: %s' %(
						serializer._from.__name__, content))
	if isinstance(ret, Exception):
		raise ret
	return ret
	
	
	
class RequestWithMethod(Request):
	'''
	Extended urllib2 request
	where method (GET,POST,PUT,DELETE) can be set as init parameter.
	'''
	def __init__(self, *args, **kwargs):
		self._url = kwargs['url']
		self._method = kwargs.pop('method', None)
		Request.__init__(self, *args, **kwargs)
	def get_method(self):
		return self._method if self._method else Request.get_method(self)

