'''
Utilities
@author Csaba Sulyok
'''

from datetime import datetime
from pytz import utc


'''
Datetime utilities
'''

epochDateTime = datetime(1970, 1, 1).replace(tzinfo=utc)

def timeToSeconds(givenDateTime):
    '''
    Converts datetime to total number of seconds.
    '''
    timeDiff = givenDateTime - epochDateTime
    return int(timeDiff.total_seconds())


def secondsToTime(seconds):
    '''
    Converts number of seconds since epoch to formatted datetime
    in the Drive API format.
    '''
    return datetime.fromtimestamp(seconds, utc)
