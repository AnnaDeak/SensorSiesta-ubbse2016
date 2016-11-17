THE example
===========

Example Software Engineering project, taken through all typical stages of SoftEng.

The different stages of the project can be accessed through [git tags](https://git-scm.com/book/en/v2/Git-Basics-Tagging).


Example Project Requirements
----------------------------
- Given are one or more *Raspberry Pis* with one or more sensor each;
- I (the client) want to visually see the readings from any device and sensor *online*, from anywhere;
- Poll intervals should be configurable on the Pi (how many times per minute each sensor sends data);
- A new Raspberry device can connect anytime and start sending data.


### 1. Project Management

The project management board for this project is hosted [here](https://waffle.io/csabasulyok/SensorSiesta-ubbse2016).


### 2. Architecture Document & Implementation Skeleton

The UML diagrams are written in *LaTeX* using the [TikzUML](http://perso.ensta-paristech.fr/~kielbasi/tikzuml/) library and built using the [Gradle LaTeX plugin](https://github.com/csabasulyok/gradle-latex). 

The tag [v0.2](https://github.com/csabasulyok/SensorSiesta-ubbse2016/tree/v0.2) contains the empty skeleton of implementation. The associated architecture can be found on the wiki [here](https://github.com/csabasulyok/SensorSiesta-ubbse2016/wiki/Architecture).
