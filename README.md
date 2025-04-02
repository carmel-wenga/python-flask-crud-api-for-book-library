# BookEx

This repo aims to build a microservice app that explores books,

* Python: version 3.10
* Flask : a python web framework that we use to build backend api
* SQLAlchemy: For the ORM
* Alembic : for the database migration
* Postgresql : a relational database that will store our data,
* Docker : to containerized our application,
* Docker Compose: For development
* Nginx as server and reserve proxy

### Steps to launch the app
Run the following commands :

Create the workspace repository and clone the project

```commandline
mkdir /home/projects/BookEx && cd /home/projects/BookEx
git clone https://github.com/carmel-wenga/python-flask-crud-api-for-book-library
```
Before being able to run the app, you need to create the virtualenv

How to install/create the virtualenv on windows and linux ? Add those steps

````commandline
mkdir lib/env
````
# Deploy the app on Docker
1. Create a Docker network that will host the frontend, the backend and the database
```commandline
docker network create libnetwork
```

2. Run Postgres container inside the libnetwork
```commandline
docker run --name database --network libnetwork --env-file .postgres.env -p 5432:5432 -d postgres
```
3. Build the backend image and run it inside the libnetwork
```commandline
docker build -t libapi:latest .
```
Then run the libapi container by specifying the environment variables related to the database

```commandline
docker run --name libapi --network libnetwork --env-file .env -p 5000:5000 -d libapi:latest
```
5. Initialize the database and run the migrations
Connect to the backend container by running the following commands

```commandline
docker exec -it libapi sh
``` 
Then run the following commands to initialize the database and run the migrations
```commandline
flask db init
flask db migrate -m "initial migrations"
flask db upgrade
```
Since the migrations folder has already been created, you only need to run the ```flask db upgrade``` command. If 
everything is ok, you should see a result similar to the one below:

```commandline
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.  
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 26496524190f, initial migration
```
6. Test the application
Go to ```http://localhost:5000/api/docs``` for more details on the description of the api.
Use the available endpoints to create a book, read a book, update a book, delete a book and get all books from the 
openapi documentation.

# Deploy the app on Docker Compose

1. Build and run the app 

```commandline
docker-compose up -d --build 
```
2. Initialize the database and run the migrations

Script ```initdb.sh``` contains the commands below to initialize the database and run the migrations

```commandline
docker-compose exec backend flask db init
docker-compose exec backend flask db migrate -m "initial migrations"
docker-compose exec backend flask db upgrade
```

Since I have already run the two first commands above, and a migrations folder has been created in the root directory, 
You only need to run the ```flask db upgrade``` command.

If you want to run all the commands, delete the ```migrations``` folder first with admin privileges.

```commandline
3. Use the following command to connect to the postgres image and inspect the contains of the database
```commandline
docker-compose exec database psql --username=pguser --dbname=bookexdb
```
Note that the username ```pguser``` and the database name ```bookexdb``` are
defined in the ```.env``` file that should contain secrets information about
the application. It should not be tracker by git.

### App Structure

This Backend App exposes 5 endpoints:

1. Create Book: endpoint is used to create a book
```commandline
curl --location --request POST 'localhost:5000/api/v1/books/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "isbn": "9780439358071",
    "title": "Harry Potter and the Order of the Phoenix",
    "authors": "J.K. Rowling, Mary GrandPré (Illustrator)",
    "description": "There is a door at the end of a silent corridor. And it’s haunting Harry Pottter’s dreams. Why else would he be waking in the middle of the night, screaming in terror?Harry has a lot on his mind for this, his fifth year at Hogwarts: a Defense Against the Dark Arts teacher with a personality like poisoned honey; a big surprise on the Gryffindor Quidditch team; and the looming terror of the Ordinary Wizarding Level exams. But all these things pale next to the growing threat of He-Who-Must-Not-Be-Named - a threat that neither the magical government nor the authorities at Hogwarts can stop.As the grasp of darkness tightens, Harry must discover the true depth and strength of his friends, the importance of boundless loyalty, and the shocking price of unbearable sacrifice.His fate depends on them all.",
    "language": "English",
    "genres": "Fantasy, Young Adult, Fiction, Magic, Childrens, Adventure, Audiobook, Middle Grade, Classics, Science Fiction Fantasy",
    "publisher": "Scholastic Inc.",
    "publish_date": "2004-09-28",
    "price": 7.38,
    "pages": 870
  }'
```
2. Read Book: Add new book in the database
```commandline
curl --location --request GET 'localhost:5000/api/v1/books/9780439358071'
```

3. Update Book
```commandline
curl --location --request PUT 'localhost:5000/api/v1/books/9780439358071' \
--header 'Content-Type: application/json' \
--data-raw '{
    "authors": "J.K. Rowling, Mary GrandPré",
    "language": "English",
    "pages": 950,
    "price": 15.38
}'
```

4. Delete Book
```commandline
curl --location --request DELETE 'localhost:5000/api/v1/books/9780439358071'
```

5. Get all book
```commandline
curl --location --request GET 'localhost:5000/api/v1/books/'
```

Go to ```http://localhost:5000/api/docs``` for more details on the description of the api.

### Project Structure
```commandline
BookEx
├── app
│   ├── api
│   │   └── v1
│   │       ├── books
│   │       │   ├── __init__.py
│   │       │   └── views.py
│   │       └── __init__.py
│   ├── domain
│   │   └── books
│   │       ├── models.py
│   │       └── utils.py
│   ├── __init__.py
│   ├── main
│   │   ├── __init__.py
│   │   └── views.py
│   └── static
│       └── yml
│           └── swagger.yml
├── books.csv
├── config.py
├── docker-compose.yml
├── Dockerfile
├── .dockerignore
├── .env
├── .gitignore
├── manage.py
├── README.md
├── requirements.txt
├── settings.py
└── utils.py
```
---
1. Entrypoint of the app

The entry point of the application is the ```app/__init__.py``` file. The code below creates the flask app, configure 
it, creates the sqlalchemy db and link both the app and the db together

```python
# create flask app
app = Flask(__name__)

# Allow CORS for all routes
CORS(app)

# import flask configurations
app.config.from_object(Config)

# create the database
db = SQLAlchemy(app)

Migrate(app, db)
```

* The ```api``` package contains only one version of the api server. The first version 
```v1```. The ```api/v1/books/views.py``` contains all the endpoints for CRUD operations on books

* The ```domain/books/models.py``` files defines the Books models and ```domain/books/utils.py```
defines useful functions on books

* ```static/yml/swagger.yml``` is the openapi documentation of the api 

# Deploy the app on Kubernetes

I have used Docker Desktop for Windows to deploy the app on Kubernetes.

## Building the Docker image

Then build the image with the following command:

```commandline
docker build -t libackend:latest .
```

## Deploying the app on Kubernetes
The app can be deployed on kubernetes using the ```k8s``` folder. 
The folder contains the following files:

* ```configmap.yaml```: The configmap file for the backend app
* ```secret.yaml```: Contains secrets for the database
* ```postgres-deployment.yaml```: The deployment file for the database
* ```postgres-service.yaml```: The service configuration file for the database
* ```postgres-pvc.yaml```: The persistent volume claim configuration file for the database
* ```backend-deployment.yaml```: the deployment configuration for the backend app
* ```backend-service.yaml```: the service configuration for the backend app

Run the command below to deploy the app on kubernetes
```commandline
$ kubectl apply -f .\k8s
```

## Database migrations

Then apply the database migrations by running the following commands:

```commandline
$ kubectl exec -it [backend-pod-name] -- flask db init
$ kubectl exec -it [backend-pod-name] -- flask db migrate -m "initial migrations"
$ kubectl exec -it [backend-pod-name] -- flask db upgrade
```
run ```kubectl get pods``` to get the backend pod name

Since the ```migrations``` folder has already been created, you only need to run the ```flask db upgrade``` command.


## Test the app

To test the app, you need to connect to the backend pod with the following command:

```commandline
kubectl exec -it [backend-pod-name] -- sh
```

Then run the following command to test creation of a book:

```commandline
curl --location --request POST 'localhost:5000/api/v1/books/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "isbn": "9780439358071",
    "title": "Harry Potter and the Order of the Phoenix",
    "authors": "J.K. Rowling, Mary GrandPré (Illustrator)",
    "description": "There is a door at the end of a silent corridor. And it’s haunting Harry Pottter’s dreams. Why else would he be waking in the middle of the night, screaming in terror?Harry has a lot on his mind for this, his fifth year at Hogwarts: a Defense Against the Dark Arts teacher with a personality like poisoned honey; a big surprise on the Gryffindor Quidditch team; and the looming terror of the Ordinary Wizarding Level exams. But all these things pale next to the growing threat of He-Who-Must-Not-Be-Named - a threat that neither the magical government nor the authorities at Hogwarts can stop.As the grasp of darkness tightens, Harry must discover the true depth and strength of his friends, the importance of boundless loyalty, and the shocking price of unbearable sacrifice.His fate depends on them all.",
    "language": "English",
    "genres": "Fantasy, Young Adult, Fiction, Magic, Childrens, Adventure, Audiobook, Middle Grade, Classics, Science Fiction Fantasy",
    "publisher": "Scholastic Inc.",
    "publish_date": "2004-09-28",
    "price": 7.38,
    "pages": 870
  }'
```
Note that I'm using localhost because I'm connected to the pod. If you want to test the app from your local machine, 
you need to expose the service to be accessible from outside the cluster.