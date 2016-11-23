'''
Depdendency management - load common to path
'''
from os.path import abspath, dirname
import sys

sys.path.append(abspath('%s/../../sensorsiesta-common' %(dirname(__file__))))
# print 'sensorsiesta-common loaded to path'
import sensorsiestacommon