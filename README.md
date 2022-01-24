# Api

## Requirements
* Postgresql instance with port 5439
* You can use `docker-compose` file for postgresql instance
* Authentication of postgres given in `docker.env` file
* Python 3.8 and higher required.

## How to install and run the project
```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt 
$ python manage.py migrate
$ python manage.py runserver
```

## How to build Docker image
```bash
$ docker build -t exchange-api:latest .
```

## How to run built image
```bash
$ docker run -p 8000:8000 exchange-api
