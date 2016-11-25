from sensorsiestaserver.flaskrest import FlaskRestServer
from sensorsiestacommon.entities import ExampleEntity
from sensorsiestacommon.utils import jsonSerializerWithUri
from sensorsiestacommon.flasksqlalchemy import sqlAlchemyFlask


if __name__ == '__main__':
    
    port = 5000
    
    # set up flask server
    flaskServer = FlaskRestServer(port = port,
                                  serializer = jsonSerializerWithUri)
    flaskServer.wire(ExampleEntity)
    
    # set up flask-sqlalchemy & create tables
    sqlAlchemyFlask.setApp(flaskServer.flaskApp)
    sqlAlchemyFlask.create_all()
    
    # start flask server on local thread
    flaskServer.start(threaded = False)
    
