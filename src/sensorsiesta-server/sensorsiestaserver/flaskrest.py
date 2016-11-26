'''
Expose REST calls through a small flask server.
@author Csaba Sulyok
'''

from os.path import abspath
from sys import stderr
from thread import start_new_thread

from flask import abort, request as flask_request
from flask.app import Flask
from flask.helpers import url_for
from flask.wrappers import Response
from sqlalchemy.orm.attributes import QueryableAttribute
from sqlalchemy.orm.relationships import RelationshipProperty

from sensorsiestacommon.flasksqlalchemy import sqlAlchemyFlask
from sensorsiestacommon.utils import isPortListening, jsonSerializerWithUri


dbsession = sqlAlchemyFlask.session


class FlaskRestServer(object):
	'''
	Small server which can be run on a different thread.
	Wires REST calls to DAOs.
	'''
	
	def __init__(self, dbUri = 'sqlite:///:memory:', port = 5000, serializer = jsonSerializerWithUri):
		self.flaskApp = Flask(__name__,
							  static_url_path='',
							  static_folder=abspath('./static'))
		self.flaskApp.config['SQLALCHEMY_DATABASE_URI'] = dbUri
		self.flaskApp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
		self.flaskApp.config['SQLALCHEMY_ECHO'] = True
		
		@self.flaskApp.route('/')
		def index():
			return self.flaskApp.send_static_file('index.html')
		
		self.port = port
		self.serializer = serializer
		self.namespaces = {}
		
		
	def wire(self, cls, namespace = None):
		'''
		Wire HTTP calls to a given class to a DAO.
		'''
		
		# assign default namespace if need be
		if namespace is None:
			clsName = cls.__name__
			namespace = clsName[0] + clsName[1:] + 's'
		
		namespaceSingle = namespace[:-1]
		
		self.namespaces[cls] = {
			'cls' : cls,
			'namespace' : namespace,
			'namespaceSingle' : namespaceSingle,
			'innerNamespaces' : {}
		}
		
		def _ok(content = {'result': True}):
			'''
			Build positive response with result:True by default
			'''
			ret = Response(self.serializer._to(content),
						   status = 200,
						   content_type = self.serializer.contentType)
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
			self.serializer.currentUri = url_for(namespace, _external=True)
			ret = _ok({namespace: cls.query.all()})
			self.serializer.currentUri = None
			return ret
		
		
		def handleGet(uid):
			'''
			Handle findById.
			'''
			self.serializer.currentUri = url_for(namespace + '_findById', uid = uid, _external=True)
			ret = _ok({namespaceSingle: cls.query.get(uid)})
			self.serializer.currentUri = None
			return ret
		
		
		def handleGetInner(uid, propName):
			'''
			Handle finding of attributes mapped with one-to-many.
			'''
			innerNamespace = self.namespaces[cls]['innerNamespaces'][propName]
			item = cls.query.get(uid)
			innerItems = getattr(item, propName).all()
			
			self.serializer.currentUri = url_for(innerNamespace['namespace'], _external=True)
			ret = _ok({innerNamespace['namespace']: innerItems})
			self.serializer.currentUri = None
			return ret
		
		
		def handlePost():
			'''
			Handle POST calls.
			If attempted prop is a list, create new element with parameters in request data.
			'''
			data = _deserializeRequestData()
			newItem = cls(**data)
			dbsession.add(newItem)
			dbsession.commit()
			dbsession.refresh(newItem)
			
			self.serializer.currentUri = url_for(namespace + '_findById', uid = newItem.uid, _external=True)
			ret = _ok({namespaceSingle: newItem})
			self.serializer.currentUri = None
			return ret
			
		
		def handlePut(uid):
			'''
			Handle PUT calls.
			If attempted prop is a dict or class instance, it gets updated based on request data.
			'''
			data = _deserializeRequestData()
			dbsession.query(cls).filter_by(uid=uid).update(data)
			dbsession.commit()
			item = cls.query.get(uid)
		
			self.serializer.currentUri = url_for(namespace + '_findById', uid = item.uid, _external=True)
			ret = _ok({namespaceSingle: item})
			self.serializer.currentUri = None
			return ret
			
			
		def handleDelete(uid):
			'''
			Handle DELETE calls.
			Deletes item with given ID.
			'''
			dbsession.delete(cls.query.get(uid))
			dbsession.commit()
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
		self.flaskApp.add_url_rule('/' + namespace + '/<int:uid>/<string:propName>',
							  namespace + '_findInner',
							  handleGetInner,
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
		
	
	
	def wireOneToMany(self, cls, innerCls, propName):
		'''
		Note that there is a one-to-many relationship between cls and innerClass
		that can be accessed in cls through propName.
		'''
		self.namespaces[cls]['innerNamespaces'][propName] = self.namespaces[innerCls]
		
		
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
