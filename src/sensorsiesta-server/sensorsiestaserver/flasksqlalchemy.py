from types import MethodType

from flask_sqlalchemy import SQLAlchemy
from pytz import utc
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql.type_api import TypeDecorator


sqlAlchemyFlask = SQLAlchemy()

def __setApp(self, app):
    self.app = app
    self.init_app(app) 
    
sqlAlchemyFlask.setApp = MethodType(__setApp, sqlAlchemyFlask)

Model = sqlAlchemyFlask.Model



class TimeZoneAwareDateTime(TypeDecorator):
    '''
    Results returned as aware datetimes, not naive ones.
    '''
    impl = DateTime
    def process_result_value(self, value, dialect):
        return value.replace(tzinfo=utc)
    
    