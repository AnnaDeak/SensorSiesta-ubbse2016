Software Engineering Example Project: Python and Flask server
-------------------------------------------------------------

This server module allows REST calls and operates an sqlite file-based database.

## Launching the server

#### 1. Set up web client files

Before first launch, make sure [`sensorsiesta-web-client`](https://github.com/csabasulyok/SensorSiesta-ubbse2016/tree/master/src/sensorsiesta-web-client) has been built, so the static HTML files this server hosts can be accessed. Check the Installation section.

#### 2. Make sure required dependencies are satisfied

This step needs to be done only once, to make sure external dependencies are downloaded.

~~~bash
pip install -r requirements.txt
~~~

If `pip` is not available, use:

~~~bash
sudo apt-get install python-pip
~~~

#### 3. Start the server

~~~bash
python app.py
~~~
