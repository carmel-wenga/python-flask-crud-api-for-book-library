from app import db
from datetime import date, datetime


class Book(db.Model):
    __tablename__ = "books"

    book_id = db.Column(db.String(50), primary_key=True)
    isbn = db.Column(db.String(50), nullable=False)
    title = db.Column(db.Text, nullable=False)
    authors = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(50), nullable=False)
    genres = db.Column(db.Text, nullable=False)
    publisher = db.Column(db.String(255), nullable=False)
    publish_date = db.Column(db.Date, nullable=False)
    price = db.Column(db.Float, nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow(),
                            onupdate=datetime.utcnow())

    def __repr__(self):
        print(f'<Book - isbn:{self.isbn}, title:{self.title}>')
