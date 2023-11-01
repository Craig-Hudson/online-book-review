from readersrealm import db

import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    password_confirmation = db.Column(db.String(255), nullable=False)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    biography = db.Column(db.Text)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.String(200))
    publication_year = db.Column(db.Integer)


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)


class BookGenre(db.Model):
    book_id = db.Column(db.Integer, db.ForeignKey(
        'book.id'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey(
        'genre.id'), primary_key=True)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    review_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
