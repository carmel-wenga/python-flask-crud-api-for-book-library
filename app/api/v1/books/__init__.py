from flask import Blueprint

books = Blueprint('books', '__name__', cli_group='books_bp')

from . import views
