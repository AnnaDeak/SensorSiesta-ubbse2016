'''
Add python-common to PYTHONPATH
'''
from os.path import abspath, dirname
import sys

sys.path.append(abspath('%s/../sensorsiesta-common' %(abspath(dirname(__file__)))))
print 'sensorsiesta-common loaded to path'

from mod import a

import rpyc

conn = rpyc.connect("localhost", 12345)
print conn.root.sub(12,5)