Software Engineering Example Project
====================================

Example Software Engineering project, taken through all typical stages except testing:

- requirement specification
- project management setup
- version control setup
- architecture
- design
- continuous integration & delivery

The different stages of the project can be accessed through [git tags](https://git-scm.com/book/en/v2/Git-Basics-Tagging).


### 1. Requirements

The example project is given the following requirements:

- Given are one or more *Raspberry Pis* with one or more sensor each;
- I (the client) want to visually see the readings from any device and sensor *online*, from anywhere;
- Poll intervals should be configurable on the Pi (how many times per minute each sensor sends data);
- A new Raspberry device can connect anytime and start sending data.


### 2. Project Management

The project management board for this project is hosted [here](https://waffle.io/csabasulyok/SensorSiesta-ubbse2016).


### 3. Architecture Document & Implementation Skeleton

The UML diagrams are written in *LaTeX* using the [TikzUML](http://perso.ensta-paristech.fr/~kielbasi/tikzuml/).

The tag [v0.2](https://github.com/csabasulyok/SensorSiesta-ubbse2016/tree/v0.2) contains the empty skeleton of implementation. The associated architecture can be found on the wiki [here](https://github.com/csabasulyok/SensorSiesta-ubbse2016/wiki/Architecture). The proposed folder structure is the following:

- [`doc`](https://github.com/csabasulyok/SensorSiesta-ubbse2016/tree/master/doc) - TeX diagrams for architecure & design on Wiki;
- [`src`](https://github.com/csabasulyok/SensorSiesta-ubbse2016/tree/master/src) - source folders
  - [`sensorsiesta-common`](https://github.com/csabasulyok/SensorSiesta-ubbse2016/tree/master/src/sensorsiesta-common) - common classes for server and Raspberry Pi client: entities and REST client;
  - [`sensorsiesta-server`](https://github.com/csabasulyok/SensorSiesta-ubbse2016/tree/master/src/sensorsiesta-server) - main server package; contains sqlite DAOs and REST service endpoint;
  - [`sensorsiesta-rpi-client`](https://github.com/csabasulyok/SensorSiesta-ubbse2016/tree/master/src/sensorsiesta-rpi-client) - Raspberry Pi client package; publishes sensor data to server;
  - [`sensorsiesta-web-client`](https://github.com/csabasulyok/SensorSiesta-ubbse2016/tree/master/src/sensorsiesta-web-client) - web client; built by Grunt and deployed into static folder of server; reads data through REST and displays it.


### 4. Design & Implementation

The tag [v0.3](https://github.com/csabasulyok/SensorSiesta-ubbse2016/tree/v0.3) contains the final implementation of the project. The associated design can be found on the wiki [here](https://github.com/csabasulyok/SensorSiesta-ubbse2016/wiki/Design). Also the READMEs in the `src` subfolders describe how to start & manage all the applications.


### 5. Continuous Integration & Delivery

The tag [v0.4](https://github.com/csabasulyok/SensorSiesta-ubbse2016/tree/v0.4) contains necessary files to set up continuous integration and deployment.

#### Docker

The server is run using a Dockerfile [here](src/Dockerfile).
From the [`src`](src) folder:

- Build the Docker image using `sudo docker build -t csabasulyok/sensorsiesta:1.0.0 .`
- Run it using `sudo docker run -p 5000:5000 --rm -it csabasulyok/sensorsiesta:1.0.0`
- Deploy to Docker Hub using `sudo docker push csabasulyok/sensorsiesta:1.0.0`

#### Travis CI

On every delivery, the continuous integration step is triggered in the form of a [Travis CI job](https://travis-ci.org/csabasulyok/SensorSiesta-ubbse2016).
This job uses the local [.travis.yml](https://github.com/csabasulyok/SensorSiesta-ubbse2016/tree/master/.travis.yml) file to build and push a Docker image.

#### Heroku

The Docker image created by Travis CI is pushed to the [Heroku registry](https://devcenter.heroku.com/articles/container-registry-and-runtime).
The associated Heroku app's dashboard can be seen [here](https://dashboard.heroku.com/apps/sensorsiesta-ubbse2016).
The application is deployed on every commit to gitHub. The latest live version is accessible here:

[`https://sensorsiesta-ubbse2016.herokuapp.com/`](https://sensorsiesta-ubbse2016.herokuapp.com/)
 