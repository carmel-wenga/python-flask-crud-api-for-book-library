# BookEx

This repo aims to build a microservice app that explores books,

* Python,
* Flask : a python web framework that can be used to build api
* Postgresql : a relational database that will store our data,
* Elasticsearch : a such engine that we will use to easily such for data into its index, 
* Jenkins: 
* Docker : to containerized our application,
* Kubernetes : use for deployment.

### Steps to launch the app
Run the following commands :
1. Build and run the app 
```commandline
docker-compose up -d --build 
```
2. Initialize the database used by the app
```commandline
docker-compose exec web flask db init
```
Create migrations with the following command
```commandline
docker-compose exec web flask db migrate -m "initial migrations"
```
Apply the migrations by doing
```commandline
docker-compose exec web flask db upgrade
```
3. Use the following command to connect to the postgres image and inspect the contains of the database
```commandline
docker-compose exec datahub psql --username=pguser --dbname=bookexdb
```
Note that the username ```pguser``` and the database name ```transactions``` are
defined in the ```.env``` file that should contain secrets information about
the application. It should not be tracker by git.

