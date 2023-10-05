from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/yml/swagger.yml'  # Our API url (can of course be a local resource)

# create flask app
app = Flask(__name__)

# Allow CORS for all routes
CORS(app)

# import flask configurations
app.config.from_object(Config)

# create the database
db = SQLAlchemy(app)

Migrate(app, db)

from app.main import main as main_bp
from app.api.v1 import api as api_v1_bp


# init and set app routes
app.register_blueprint(main_bp)
app.register_blueprint(api_v1_bp, url_prefix='/api')

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "BookEx",
        'description': "This application is for Book exploration. Five endpoints: Add, Get, GetAll, Update, Delete"
    }
)

app.register_blueprint(swaggerui_blueprint)
