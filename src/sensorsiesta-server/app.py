from sensorsiestaserver.flaskrest import FlaskRestServer
from sensorsiestacommon.entities import ExampleEntity, ExampleInnerEntity,\
    SensorReading, Sensor, SensorType, RPi
from sensorsiestacommon.utils import jsonSerializerWithUri
from sensorsiestacommon.flasksqlalchemy import sqlAlchemyFlask


if __name__ == '__main__':
    
    port = 5000
    
    # set up flask server
    flaskServer = FlaskRestServer(dbUri = 'sqlite:///test.db',
                                  port = port,
                                  serializer = jsonSerializerWithUri)
    
    # wire entities
    flaskServer.wire(SensorReading)
    flaskServer.wire(Sensor)
    flaskServer.wire(SensorType)
    flaskServer.wire(RPi)
    flaskServer.wireOneToMany(RPi, Sensor, 'sensors')
    flaskServer.wireOneToMany(SensorType, Sensor, 'sensors')
    flaskServer.wireOneToMany(Sensor, SensorReading, 'readings')
    
    
    # set up flask-sqlalchemy & create tables
    sqlAlchemyFlask.setApp(flaskServer.flaskApp)
    sqlAlchemyFlask.create_all()
    
    # start flask server on local thread
    flaskServer.start(threaded = False)
    
