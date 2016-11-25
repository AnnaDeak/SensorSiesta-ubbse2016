from datetime import datetime

from flask.app import Flask
from pytz import utc
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String

from sensorsiestacommon.flasksqlalchemy import Model, sqlAlchemyFlask
from sensorsiestacommon.utils import jsonSerializer


app = Flask('app')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

sqlAlchemyFlask.setApp(app)

class A(Model):
    id = Column(Integer, primary_key = True)
    mem = Column(String)
    
sqlAlchemyFlask.create_all()

session = sqlAlchemyFlask.session

a = A()
a.mem = 'abc'
session.add(a)
session.commit()
session.refresh(a)


a = A.query.get(1)


newProps = {'mem' : 'newabc'}
session.query(A).filter_by(id=1).update(newProps)
#a.mem = 'newabc'

session.commit()
session.refresh(a)

print a.id, a.mem