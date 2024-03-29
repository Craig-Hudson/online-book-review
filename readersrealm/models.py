from readersrealm import db

import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    password_confirmation = db.Column(db.String(255), nullable=False)
    reviews = db.relationship('Review', backref='user_reviews', lazy=True)
    books = db.relationship('Book', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    genre = db.Column(db.String(200))
    description = db.Column(db.String(2500))
    publication_year = db.Column(db.Integer)
    image_url = db.Column(db.String(2000), default='not-available.webp')
    author = db.relationship('Author', backref='books')
    reviews = db.relationship('Review', cascade='delete')


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
    user = db.relationship('User', backref='user_reviews')
    book = db.relationship('Book', backref='user_reviews')
