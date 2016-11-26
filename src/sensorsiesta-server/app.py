from sensorsiestaserver.flaskrest import FlaskRestServer
from sensorsiestacommon.entities import ExampleEntity, ExampleInnerEntity
from sensorsiestacommon.utils import jsonSerializerWithUri
from sensorsiestacommon.flasksqlalchemy import sqlAlchemyFlask


if __name__ == '__main__':
    
    port = 5000
    
    # set up flask server
    flaskServer = FlaskRestServer(dbUri = 'sqlite:///test.db',
                                  port = port,
                                  serializer = jsonSerializerWithUri)
    flaskServer.wire(ExampleInnerEntity)
    flaskServer.wire(ExampleEntity)
    flaskServer.wireOneToMany(ExampleEntity, ExampleInnerEntity, 'inners')
    
    # set up flask-sqlalchemy & create tables
    sqlAlchemyFlask.setApp(flaskServer.flaskApp)
    sqlAlchemyFlask.create_all()
    
    # start flask server on local thread
    flaskServer.start(threaded = False)
    
