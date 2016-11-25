from datetime import datetime

from flask.app import Flask
from pytz import utc
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.orm import relationship

from sensorsiestacommon.flasksqlalchemy import Model, sqlAlchemyFlask
from sensorsiestacommon.utils import jsonSerializer
from sensorsiestacommon.entities import ExampleEntity, ExampleInnerEntity


app = Flask('app')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensorsiestaserver/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

sqlAlchemyFlask.setApp(app)

sqlAlchemyFlask.create_all()
session = sqlAlchemyFlask.session

a1 = ExampleEntity()
a1.strMember = 'I am a1'
a2 = ExampleEntity()
a2.strMember = 'I am a2'
b1 = ExampleInnerEntity()
b1.strMember = 'I am b1'
b2 = ExampleInnerEntity()
b2.strM = 'I am b2'
a1.inners = [b1, b2]

session.add(a1)
session.add(a2)
session.commit()
