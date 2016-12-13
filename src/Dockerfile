# Docker build script for the Sensor Siesta server.

# Start with Python 2.7.9 image
FROM python:2.7.9

# Expose the port Flask uses (by default 5000)
EXPOSE 5000

# Copy sources to virtual machine
# local folder will become /usr/src/sensorsiesta on Docker image
RUN mkdir /usr/src/sensorsiesta
COPY sensorsiesta-common /usr/src/sensorsiesta/sensorsiesta-common
COPY sensorsiesta-server /usr/src/sensorsiesta/sensorsiesta-server

# Take care of python requirements
RUN pip install -r /usr/src/sensorsiesta/sensorsiesta-server/requirements.txt

# Start web backend
WORKDIR /usr/src/sensorsiesta/sensorsiesta-server
CMD ["python", "app.py"]
