from flask import Blueprint
from .books import books as books_bp

api = Blueprint('api', '__name__')
api.register_blueprint(books_bp, url_prefix='/v1/books')

from app.api.v1.books import views
