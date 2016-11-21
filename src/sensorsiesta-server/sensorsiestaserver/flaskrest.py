'''
Expose REST calls through a small flask server.
@author Csaba Sulyok
'''

from thread import start_new_thread
from sys import stderr
from sensorsiestaserver.utils import jsonSerializer, isPortListening
from os.path import abspath
from flask import abort, request as flask_request
from flask.app import Flask
from flask.wrappers import Response
from flask.helpers import url_for


class FlaskRestServer(object):
	'''
	Small server which can be run on a different thread.
	Wires REST calls to DAOs.
	'''
	
	def __init__(self, daoContainer, port = 5000, serializer = jsonSerializer):
		self.flaskApp = Flask(__name__,
							  static_url_path='',
							  static_folder=abspath('./static'))
		@self.flaskApp.route('/')
		def index():
			return self.flaskApp.send_static_file('index.html')
		
		self.daoContainer = daoContainer
		self.port = port
		self.serializer = serializer
		
		
	def wire(self, cls, namespace = None):
		'''
		Wire HTTP calls to a given class to a DAO.
		'''
		
		# retrieve dao of class
		dao = self.daoContainer.daoFor(cls)
		# assign default namespace if need be
		if namespace is None:
			clsName = cls.__name__
			namespace = clsName[0] + clsName[1:] + 's'
			namespaceSingle = clsName[0] + clsName[1:]
		
		
		def _ok(content = {'result': True}):
			'''
			Build positive response with result:True by default
			'''
			self.serializer.currentUri = url_for(namespace, _external=True)
			ret = Response(self.serializer._to(content),
						   status = 200,
						   content_type = self.serializer.contentType)
			self.serializer.currentUri = None
			return ret
			
			
		def _abort(exceptionText):
			'''
			Create response with an error.
			Serialize exception to be sent to caller.
			'''
			self.currentError = exceptionText
			abort(400)
				
			
		def _deserializeRequestData():
			'''
			Takes request data (be it POST or PUT) and deserializes it using given method.
			'''
			if flask_request.get_data() is '':
				return {}
			
			# if there is POST/PUT data, it should be serialized using expected method
			if str(flask_request.headers['Content-Type']) != self.serializer.contentType:
				_abort('Request Content-Type does not match expected: %s!=%s' % (
									  flask_request.headers['Content-Type'], self.serializer.contentType))
			try:
				# deserialize data
				ret = self.serializer._from(flask_request.get_data())
			except:
				_abort('Could not deserialize data %s using deserialization method %s' % (
									  flask_request.get_data(), self.serializer._from.__name__))
				
			return ret
		
		
		def handleGetAll():
			'''
			Fetch a variable dynamically when GET call comes in.
			Simply return serialized version
			'''
			return _ok({namespace: dao.findAll()})
		
		
		def handleGet(uid):
			'''
			Handle findById.
			'''
			return _ok({namespaceSingle: dao.findById(uid)})
		
		
		def handlePost():
			'''
			Handle POST calls.
			If attempted prop is a list, create new element with parameters in request data.
			'''
			data = _deserializeRequestData()
			newItem = dao.createByValues(**data)
			return _ok({namespaceSingle: newItem})
			
		
		def handlePut(uid):
			'''
			Handle PUT calls.
			If attempted prop is a dict or class instance, it gets updated based on request data.
			'''
			data = _deserializeRequestData()
			updatedItem = dao.updateByValues(uid, **data)
			return _ok({namespaceSingle: updatedItem})
			
			
		def handleDelete(uid):
			'''
			Handle DELETE calls.
			Deletes item with given ID.
			'''
			dao.deleteById(uid)
			return _ok()
		
		
		
		'''
		Add HTTP hooks.
		'''
		self.flaskApp.add_url_rule('/' + namespace,
							  namespace,
							  handleGetAll,
							  methods=['GET'])
		self.flaskApp.add_url_rule('/' + namespace + '/<int:uid>',
							  namespace + '_findById',
							  handleGet,
							  methods=['GET'])
		self.flaskApp.add_url_rule('/' + namespace,
							  namespace + '_create',
							  handlePost,
							  methods=['POST'])
		self.flaskApp.add_url_rule('/' + namespace + '/<int:uid>',
							  namespace + '_update',
							  handlePut,
							  methods=['PUT'])
		self.flaskApp.add_url_rule('/' + namespace + '/<int:uid>',
							  namespace + '_delete',
							  handleDelete,
							  methods=['DELETE'])
		
		print 'Wired: http://localhost:%d/%s' %(self.port, namespace)
		
	
	
	def start(self, threaded = True):
		'''
		Launch server.
		'''
	
		def _handleBadRequest(error):
			'''
			Create response with an error.
			Serialize exception to be sent to caller.
			'''
			e = ServerException(self.currentError)
			stderr.write('Server Exception: %s\n' % e)
			return Response(self.serializer._to(e),
						    status=400,
						    content_type=self.serializer.contentType)
			
		# handle 400 error
		self.flaskApp.register_error_handler(400, _handleBadRequest)
		
		print 'Starting server'
		if isPortListening(port = self.port):
			raise ServerException('Port %d already is use' % self.port)
		
		if threaded:
			# start http server on different thread so current one can go on changing the variables.
			start_new_thread(self.flaskApp.run, ('0.0.0.0', self.port))
		else:
			self.flaskApp.run('0.0.0.0', self.port)
	


class ServerException(Exception):
	'''
	Exceptions that get thrown by a server and are read by a client.
	Here since simple Exception is not serializable.
	'''
	def __init__(self, msg=''):
		self.msg = msg
	def __str__(self):
		return self.msg
