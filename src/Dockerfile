# Docker build script for the Sensor Siesta server.

# Start with Python 2.7.9 image
FROM python:2.7.9

# Expose the port Flask uses (by default 5000)
EXPOSE 5000

# Take care of base tool requirements
RUN apt-get update
RUN apt-get -y install npm
RUN cp /usr/bin/nodejs /usr/bin/node
RUN npm install -g grunt-cli

# Copy sources to virtual machine
# local folder will become /usr/src/sensorsiesta on Docker image
COPY . /usr/src/sensorsiesta

# Installing web frontend static files
RUN cd /usr/src/sensorsiesta/sensorsiesta-web-client && npm install && grunt deploy

# Take care of python requirements
RUN pip install -r /usr/src/sensorsiesta/sensorsiesta-server/requirements.txt

# Start web backend
WORKDIR /usr/src/sensorsiesta/sensorsiesta-server
CMD ["python", "app.py"]
