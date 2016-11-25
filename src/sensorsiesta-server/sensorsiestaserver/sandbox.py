from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer

from sensorsiestacommon.flasksqlalchemy import Model
from sensorsiestacommon.utils import jsonSerializer
from datetime import datetime
from pytz import utc


print datetime(1970, 1, 1).replace(tzinfo=utc).tzinfo
print datetime.now(utc).tzinfo