from settings import BASEDIR
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(BASEDIR, '.env'))


class Config(object):
    FLASK_ENV = 'development'
    TESTING = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    # Database
    SQLALCHEMY_DATABASE_URI = "postgresql://{user}:{password}@{host}:{port}/{db_name}".format(
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        host=os.environ.get("POSTGRES_HOST"),
        port=os.environ.get("POSTGRES_PORT"),
        db_name=os.environ.get("POSTGRES_DB")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


