'''
Add python-common to PYTHONPATH
'''
from os.path import abspath, dirname
import sys

sys.path.append(abspath('%s/../sensorsiesta-common' %(abspath(dirname(__file__)))))
print 'sensorsiesta-common loaded to path'
print sys.path

from mod import a

print 'Hello World!'
a()