from flask_sqlalchemy import SQLAlchemy
from types import MethodType


sqlAlchemyFlask = SQLAlchemy()

def __setApp(self, app):
    self.app = app
    self.init_app(app) 
    
sqlAlchemyFlask.setApp = MethodType(__setApp, sqlAlchemyFlask)

Model = sqlAlchemyFlask.Model
