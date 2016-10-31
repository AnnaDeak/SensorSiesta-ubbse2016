'''
Add python-common to PYTHONPATH
'''
from os.path import abspath, dirname
import sys

sys.path.append(abspath('%s/../sensorsiesta-common' %(abspath(dirname(__file__)))))
print 'sensorsiesta-common loaded to path'

from mod import a


from rpyc import Service
from rpyc.utils.server import ThreadedServer

class CalculatorService(Service):
    def exposed_add(self, a, b):
        return a + b
    def exposed_sub(self, a, b):
        return a - b
    def exposed_mul(self, a, b):
        return a * b
    def exposed_div(self, a, b):
        return a / b
    def foo(self):
        print "foo"


if __name__ == '__main__':
    ThreadedServer(CalculatorService, port = 12345).start()
