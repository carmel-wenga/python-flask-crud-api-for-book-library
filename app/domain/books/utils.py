from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from typing import List
from datetime import datetime

from app.domain.books.models import Book
from app import db

import uuid


def build_book(data: dict) -> Book:
    return Book(
            book_id=str(uuid.uuid4()), isbn=data.get('isbn'), title=data.get('title'), authors=data.get('authors'),
            description=data.get('description'), language=data.get('language'), genres=data.get('genres'),
            publisher=data.get('publisher'), publish_date=data.get('publish_date'), price=float(data.get('price')),
            pages=int(data.get('pages')), creation_date=datetime.utcnow(), last_update=datetime.utcnow()
        )


def get(isbn) -> Book | None:
    try:
        return db.session.query(Book).filter_by(isbn=isbn).one()
    except NoResultFound:
        return None


def get_all() -> List[Book]:
    return db.session.query(Book).all()


def update(book: Book, data: dict) -> int:

    if data.get('title'):
        book.title = data.get('title')
    if data.get('authors'):
        book.authors = data.get('authors')
    if data.get('price'):
        book.price = data.get('price')
    if data.get('description'):
        book.description = data.get('description')
    if data.get('publisher'):
        book.publisher = data.get('publisher')
    if data.get('genres'):
        book.genres = data.get('genres')
    if data.get('language'):
        book.language = data.get('language')
    if data.get('pages'):
        book.pages = data.get('pages')
    if data.get('creation_date'):
        book.creation_date = data.get('creation_date')
    if data.get('publish_date'):
        book.publish_date = data.get('publish_date')

    book.last_update = datetime.utcnow()

    try:
        db.session.commit()
        return 1
    except SQLAlchemyError as error:
        db.session.rollback()
        return 0


def add(book: Book) -> int:
    try:
        if get(book.isbn) is None:
            db.session.add(book)
            db.session.commit()
            status = 1
        else:
            status = 0
    except SQLAlchemyError as error:
        db.session.rollback()
        status = 0

    return status


def delete(isbn: str) -> int:
    try:
        book_to_delete = get(isbn)
        if book_to_delete:
            db.session.delete(book_to_delete)
            db.session.commit()
            status = 1
        else:
            status = 0
    except SQLAlchemyError as error:
        db.session.rollback()
        status = 0
    return status
