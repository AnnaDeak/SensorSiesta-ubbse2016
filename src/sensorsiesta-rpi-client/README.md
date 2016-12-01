Software Engineering Example Project: Raspberry Pi Client
---------------------------------------------------------

This client module broadcasts data to a given server.

## Launching the client

#### 1. Make sure required dependencies are satisfied

This step needs to be done only once, to make sure external dependencies are downloaded.

~~~bash
pip install -r requirements.txt
~~~

If `pip` is not available, use:

~~~bash
sudo apt-get install python-pip
~~~

#### 3. Register sensors to server

~~~bash
python register.py -n <pinNumber> [-i <interval> -s <serverHost> -p <serverPort>]
~~~

You can remove the current device's registrations using

~~~bash
python register.py -c [-s <serverHost> -p <serverPort>]
~~~


#### 4. Run the app

~~~bash
python app.py [-s <serverHost> -p <serverPort>]
~~~
