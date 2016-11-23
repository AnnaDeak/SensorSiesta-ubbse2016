'''
Asynchronous objects.
@author Csaba Sulyok
'''

import inspect
import types
from Queue import Queue
from threading import Thread


class AsyncObject(object):
	'''
	Make an object asynchronous, i.e. create a separate thread for the object
	and run all methods on said thread.
	Calls to the AsyncObject schedule the call, exit immediately and ignore the return values.
	Uses consumer-producer pattern.
	'''
	
	class DynMethod(object):
		'''
		Dynamic method.
		One is added to the async object for each method of the underlying object.
		'''
		
		def __init__(self, queue, methodName, method):
			self.queue = queue
			self.methodName = methodName
			self.method = method
			
		def __schedule__(self, *args, **kwargs):
			'''
			Schedule this method to run with given arguments.
			Only adds tuple to queue and exits.
			'''
			#remove dynobject self from args
			args = args[1:]
			self.queue.put((self, args, kwargs))
			
			
		def __call__(self, *args, **kwargs):
			'''
			Perform actual method call.
			Called from worker thread.
			'''
			self.method(*args, **kwargs)
	
	
	def __init__(self, obj):
		self.obj = obj
		# initialize queue
		self.queue = Queue()
		# create methods in local object for all methods in underlying object
		self.__patch__()
		# create and start worker thread
		self.thread = Thread(target=self._worker)
		self.thread.daemon = True
		self.thread.start()
		
	
	def __patch__(self):
		'''
		Patch async objects to have all methods that underlying object has.
		But instead of calling said methods directly, they only schedule them to run.
		'''
		# gather all methods by introspection
		methods = inspect.getmembers(self.obj, predicate=inspect.ismethod)
		
		for methodName, method in methods:
			# create dynamic method for each
			dynmethod = AsyncObject.DynMethod(self.queue, methodName, method)
			# hook method of dynamic object to scheduling
			self.__setattr__(methodName, types.MethodType(dynmethod.__schedule__, self))
	
	
	def _worker(self):
		'''
		Worker thread method.
		Implements the consumer part.
		Waits for the queue to get a task and executes it.
		'''
		while True:
			dynmethod, args, kwargs = self.queue.get()
			dynmethod.__call__(*args, **kwargs)
			self.queue.task_done()
	
	
	def join(self):
		'''
		Wait for remaining tasks to be finished and join
		the worker thread.
		'''
		self.queue.join()


