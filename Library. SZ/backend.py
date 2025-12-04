from flask import Flask,render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

library = Flask(__name__)
library.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db = SQLAlchemy(library)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)


class Magazine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    issue = db.Column(db.String(50), nullable=False)   # номер выпуска
    publisher = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(100))

@library.route('/')
def index():
    return render_template('index.html')

@library.route('/books', methods=['GET', 'POST'])
def books():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = int(request.form['year'])
        new_book = Book(title=title, author=author, year=year)
        db.session.add(new_book)
        db.session.commit()
        return redirect('/books')

    title_q = request.args.get('title', '').strip()
    year_q = request.args.get('year', '').strip()
    author_q = request.args.get('author', '').strip()

    query = Book.query

    if title_q:
        query = query.filter(Book.title.ilike(f"%{title_q}%"))
    if year_q:
        try:
            query = query.filter(Book.year == int(year_q))
        except ValueError:
            query = query.filter(False)
    if author_q:
        query = query.filter(Book.author.ilike(f"%{author_q}%"))

    books = query.all()
    return render_template('index.html', mode="books", items=books)

@library.route('/delete_book/<int:id>')
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return redirect('/books')

@library.route('/magazines', methods=['GET', 'POST'])
def magazines():
    if request.method == 'POST':
        title = request.form['title']
        issue = request.form['issue']
        publisher = request.form['publisher']
        year = int(request.form['year'])
        new_magazine = Magazine(title=title, issue=issue, publisher=publisher, year=year)
        db.session.add(new_magazine)
        db.session.commit()
        return redirect('/magazines')

    title_q = request.args.get('title', '').strip()
    year_q = request.args.get('year', '').strip()
    publisher_q = request.args.get('publisher', '').strip()

    query = Magazine.query

    if title_q:
        query = query.filter(Magazine.title.ilike(f"%{title_q}%"))
    if year_q:
        try:
            query = query.filter(Magazine.year == int(year_q))
        except ValueError:
            query = query.filter(False)
    if publisher_q:
        query = query.filter(Magazine.publisher.ilike(f"%{publisher_q}%"))

    magazines = query.all()
    return render_template('index.html', mode="magazines", items=magazines)

@library.route('/delete_magazine/<int:id>')
def delete_magazine(id):
    magazine = Magazine.query.get_or_404(id)
    db.session.delete(magazine)
    db.session.commit()
    return redirect('/magazines')


@library.route('/films', methods=['GET', 'POST'])
def films():
    if request.method == 'POST':
        title = request.form['title']
        director = request.form['director']
        year = int(request.form['year'])
        genre = request.form['genre']
        new_film = Film(title=title, director=director, year=year, genre=genre)
        db.session.add(new_film)
        db.session.commit()
        return redirect('/films')

    title_q = request.args.get('title', '').strip()
    year_q = request.args.get('year', '').strip()
    director_q = request.args.get('director', '').strip()

    query = Film.query

    if title_q:
        query = query.filter(Film.title.ilike(f"%{title_q}%"))
    if year_q:
        try:
            query = query.filter(Film.year == int(year_q))
        except ValueError:
            query = query.filter(False)
    if director_q:
        query = query.filter(Film.director.ilike(f"%{director_q}%"))

    films = query.all()
    return render_template('index.html', mode="films", items=films)

@library.route('/delete_film/<int:id>')
def delete_film(id):
    film = Film.query.get_or_404(id)
    db.session.delete(film)
    db.session.commit()
    return redirect('/films')

if __name__ == '__main__':
    with library.app_context():
        db.create_all()
    library.run(debug=True)