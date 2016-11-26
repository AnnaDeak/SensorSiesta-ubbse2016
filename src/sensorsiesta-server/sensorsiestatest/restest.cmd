cls

rem create a few
curl -i -H "Content-Type: application/json" -X POST -d "{}" http://localhost:5000/ExampleEntitys
curl -i -H "Content-Type: application/json" -X POST -d "{\"intMember\":650, \"floatMember\":22.22}" http://localhost:5000/ExampleEntitys
curl -i -H "Content-Type: application/json" -X POST -d "{\"strMember\":\"overwritten string member\"}" http://localhost:5000/ExampleEntitys

rem findAll
curl -i http://127.0.0.1:5000/ExampleEntitys

rem findById
curl -i http://127.0.0.1:5000/ExampleEntitys/2

rem update
curl -i -H "Content-Type: application/json" -X PUT -d "{\"strMember\":\"updated string member\"}" http://localhost:5000/ExampleEntitys/2

rem delete
curl -i -X DELETE http://localhost:5000/ExampleEntitys/1
curl -i -X DELETE http://localhost:5000/ExampleEntitys/3
curl -i http://127.0.0.1:5000/ExampleEntitys


rem productive dummy data
curl -i -H "Content-Type: application/json" -X POST -d "{\"host\":\"dummyHost\"}" http://localhost:5000/RPis
curl -i -H "Content-Type: application/json" -X POST -d "{\"name\":\"dummyType\"}" http://localhost:5000/SensorTypes
curl -i -H "Content-Type: application/json" -X POST -d "{\"sensorTypeUid\":1, \"rpiUid\":1}" http://localhost:5000/Sensors
curl -i -H "Content-Type: application/json" -X POST -d "{\"sensorUid\":1, \"value\":0.5}" http://localhost:5000/SensorReadings
curl -i -H "Content-Type: application/json" -X POST -d "{\"sensorUid\":1, \"value\":0.75}" http://localhost:5000/SensorReadings
curl -i -H "Content-Type: application/json" -X POST -d "{\"sensorUid\":1, \"value\":0.8}" http://localhost:5000/SensorReadings
