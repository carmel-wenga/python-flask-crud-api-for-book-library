# BookEx

This repo aims to build a microservice app that explores books,

* Python,
* Flask : a python web framework that can be used to build api
* Postgresql : a relational database that will store our data,
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
Note that the username ```pguser``` and the database name ```bookexdb``` are
defined in the ```.env``` file that should contain secrets information about
the application. It should not be tracker by git.

### App Structure

This Backend App exposes 5 endpoints:

1. Create Book: endpoint is used to create a book
```commandline
curl --location --request POST '172.23.0.3:5000/api/v1/books/' \
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
curl --location --request GET '172.23.0.3:5000/api/v1/books/9780439358071'
```

3. Update Book
```commandline
curl --location --request PUT '172.23.0.3:5000/api/v1/books/9780439358071' \
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
curl --location --request DELETE '172.23.0.3:5000/api/v1/books/9780439358071'
```

5. Get all book
```commandline
curl --location --request GET '172.23.0.3:5000/api/v1/books/'
```

Go to ```http://172.23.0.3:5000/api``` for more details on the description of the api.

where ```172.23.0.3``` is my local ip address. It might be different for yours.

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

* The ```api``` package contains only one version of the api server. The first version 
```v1```. The ```api/v1/books/views.py``` contains all the endpoints for CRUD operations on books

* The ```domain/books/models.py``` files defines the Books models and ```domain/books/utils.py```
defines useful functions on books

* ```static/yml/swagger.yml``` is the openapi documentation of the api 