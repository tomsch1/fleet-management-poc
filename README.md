# fleet-management-poc
This a poc for a fleet management api written in Python3 based on the flask framework. The second application is to test the api endpoints by manipulating some of the data.

## Build
To build the application create a new virtualenvironment and install the dependencies by running ˋpip3 install -r requirements.txtˋ.

## Run
Run the application with ˋpython3 api.pyˋ and ˋpython3 test_app.py 127.0.0.1ˋ. The argument in the latter one provides the host of the api.

## Containerized
There are Dockerfiles for each application provided and a docker-compose.yaml to orchestrate them. The test application can be run multiple times by running multiple containers of the test application image: ˋdocker-compose up -d --scale test=5ˋ for example.
