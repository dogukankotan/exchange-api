# Api


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
