Software Engineering Example Project: Web client
------------------------------------------------

This web client allows REST calls and data display using [`sensorsiesta-server`](https://github.com/csabasulyok/SensorSiesta-ubbse2016/tree/master/src/sensorsiesta-server).


## Installation

Before launching the server, the current project must be `installed` into the static folder of the server.


#### 1. Tools

First, make sure you have `npm` and `grunt` installed on your system.

If `npm` is not on `PATH`:

~~~bash
sudo apt-get install npm
sudo cp /usr/bin/nodejs /usr/bin/node
~~~

If `grunt` is not on `PATH`:

~~~bash
sudo npm install -g grunt-cli
~~~


#### 2. Load dependencies of web module (jQuery, Bootstrap etc.)

Call from current folder:

~~~bash
npm install
~~~


#### 3. Install static files

~~~bash
grunt deploy
~~~

For debug build (no minifying), use

~~~bash
grunt debugDeploy
~~~

Now you can start the server.
