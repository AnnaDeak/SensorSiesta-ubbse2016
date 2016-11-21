'''
Make Python process monitorable.
Uses flask to host a small web server on a separate thread.
Variables can be wired to this server, and their status monitored through http.
'''

from thread import start_new_thread

from sys import stderr
from sensorsiestaserver.utils import jsonSerializer, isPortListening
from os.path import abspath
from flask import abort, request as flask_request
from flask.app import Flask
from flask.wrappers import Response
from flask.helpers import url_for


flaskApp = Flask(__name__,
				 static_url_path='',
				 static_folder=abspath('./static'))
monitorState = {}



def wire(namespace,
		 dao,
		 serializer = jsonSerializer):
	
	def _ok(content = {'result': True}):
		'''
		Build positive response with result:True by default
		'''
		serializer.currentUri = url_for(namespace, _external=True)
		ret = Response(serializer._to(content),
					   status=200,
					   content_type=serializer.contentType)
		serializer.currentUri = None
		return ret
		
		
	def _abort(exceptionText):
		'''
		Create response with an error.
		Serialize exception to be sent to caller.
		'''
		monitorState['currentError'] = exceptionText
		abort(400)
			
		
	def _deserializeRequestData():
		'''
		Takes request data (be it POST or PUT) and deserializes it using given method.
		'''
		if flask_request.get_data() is '':
			return {}
		
		# if there is POST/PUT data, it should be serialized using expected method
		if str(flask_request.headers['Content-Type']) != serializer.contentType:
			_abort('Request Content-Type does not match expected: %s!=%s' % (
								  flask_request.headers['Content-Type'], serializer.contentType))
		try:
			# deserialize data
			ret = serializer._from(flask_request.get_data())
		except:
			_abort('Could not deserialize data %s using deserialization method %s' % (
								  flask_request.get_data(), serializer._from.__name__))
			
		return ret
	
	
	def handleGetAll():
		'''
		Fetch a variable dynamically when GET call comes in.
		Simply return serialized version
		'''
		return _ok(dao.findAll())
	
	
	def handleGet(uid):
		'''
		Handle findById.
		'''
		return _ok(dao.findById(uid))
	
	
	def handlePost():
		'''
		Handle POST calls.
		If attempted prop is a list, create new element with parameters in request data.
		'''
		data = _deserializeRequestData()
		newItem = dao.createByValues(**data)
		return _ok(newItem)
		
	
	def handlePut(uid):
		'''
		Handle PUT calls.
		If attempted prop is a dict or class instance, it gets updated based on request data.
		'''
		data = _deserializeRequestData()
		updatedItem = dao.updateByValues(uid, **data)
		return _ok(updatedItem)
		
		
	def handleDelete(uid):
		'''
		Handle DELETE calls.
		Deletes item with given ID.
		'''
		dao.deleteById(uid)
		return _ok()
	
	
	
	flaskApp.add_url_rule('/' + namespace,
						  namespace,
						  handleGetAll,
						  methods=['GET'])
	flaskApp.add_url_rule('/' + namespace + '/<int:uid>',
						  namespace + '_findById',
						  handleGet,
						  methods=['GET'])
	flaskApp.add_url_rule('/' + namespace,
						  namespace + '_create',
						  handlePost,
						  methods=['POST'])
	flaskApp.add_url_rule('/' + namespace + '/<int:uid>',
						  namespace + '_update',
						  handlePut,
						  methods=['PUT'])
	flaskApp.add_url_rule('/' + namespace + '/<int:uid>',
						  namespace + '_delete',
						  handleDelete,
						  methods=['DELETE'])
	print 'Wired', namespace
	


def expose(port=5000,
		   serializer=jsonSerializer,
		   threaded=True):

	def _ok(content={'result': True}):
		'''
		Build positive response with result:True by default
		'''
		return Response(serializer._to(content),
					    status=200,
					    content_type=serializer.contentType)
	
	
	def _handleBadRequest(error):
		'''
		Create response with an error.
		Serialize exception to be sent to caller.
		'''
		e = ServerException(monitorState['currentError'])
		stderr.write('Server Exception: %s\n' % e)
		return Response(serializer._to(e),
					    status=400,
					    content_type=serializer.contentType)
		
		
	# handle 400 error
	flaskApp.register_error_handler(400, _handleBadRequest)
	
	# start http server on different thread so current one can go on changing the variables.
	print 'Starting server'
	if isPortListening(port=port):
		raise ServerException('Port %d already is use' % port)
	
	if threaded:
		start_new_thread(flaskApp.run, ('0.0.0.0', port))
	else:
		flaskApp.run('0.0.0.0', port)
	

class ServerException(Exception):
	'''
	Exceptions that get thrown by a server and are read by a client.
	Here since simple Exception is not serializable.
	'''
	def __init__(self, msg=''):
		self.msg = msg
	def __str__(self):
		return self.msg
