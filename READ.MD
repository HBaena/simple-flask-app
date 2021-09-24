# Simle API to measure distance between an origins address to MKAD

## Packages and extensions
- Flask
- Flask-restful
- Flask-apispec
- Marshmallow
- Gunicorn
- Google maps api
- Swagger

## First steps
- Install dependencies (I recommend to use a virtual enviroment)
```shell
pip install -r requirements.txt
```
### Run locally
- Flask server
```shell
export FLASK_ENV=development
python wsgi.py # or flask run --port 5000 --reload
```
- Gunicorn server
```shell
gunicorn -c gunicorn.config.py -b 0.0.0.0:5000 wsgi:app --reload
```
### Simple deploy using Docker and Gunicorn (Docker installation is needed)
```shell
docker build --tag my-flask-app .
dcoker run -d -p 5000:5000 my-flask-app
```

## Docs
Once with the app running, you can get the swagger doc by using `0.0.0.0:5000/docs/` in json or a UI on `0.0.0.0/docs-ui/`

## Unit tests
Unit tests are made using unittest python framework. Can be checked by
```shell
python -m unittest
```
Are divided into two groups: Api tests and functions tests.

### API Tests
These tests check how the app could response when certain valid and invalid address are sent, address that are not measurable or if no address are sent.

### Functions Tests
These tests check how functions validate type hinting, what they returns when no coords are sent, what exceptions raise or if the returned values are correct.