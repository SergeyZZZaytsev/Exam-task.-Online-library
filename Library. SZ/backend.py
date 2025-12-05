from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

library = Flask(__name__)
library.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db = SQLAlchemy(library)

# ---------- MODELS ----------
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rank = db.Column(db.Integer, nullable=True)

class Magazine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    issue = db.Column(db.String(50), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rank = db.Column(db.Integer, nullable=True)

class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(100))
    rank = db.Column(db.Integer, nullable=True)

# ---------- ROUTES ----------
@library.route('/')
def index():
    return render_template('index.html')

# ----- BOOKS -----
@library.route('/books', methods=['GET', 'POST'])
def books():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = int(request.form['year'])

       
        last_rank = db.session.query(db.func.max(Book.rank)).scalar()
        new_rank = (last_rank or 0) + 1

        new_book = Book(title=title, author=author, year=year, rank=new_rank)
        db.session.add(new_book)
        db.session.commit()
        return redirect('/books')
    
    search_q = request.args.get('search', '').strip()
    query = Book.query
    if search_q:
        query = query.filter(
            (Book.title.ilike(f"%{search_q}%")) |
            (Book.author.ilike(f"%{search_q}%")) |
            (Book.year.like(search_q))
        )

    books = query.order_by(Book.rank).all()

    matched_ranks = [b.rank for b in books]
    if matched_ranks:
        message = f" Books with rank : {', '.join(map(str, matched_ranks))}"
    else:
        message = ("Nothing found")
        
    return render_template(
        'index.html',
        mode="books",
        items=books,
        message=message,
        search_mode=bool(search_q))

@library.route('/delete_book/<int:id>')
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()

    books = Book.query.order_by(Book.rank).all()
    for i, b in enumerate(books, start=1):
        b.rank = i
    db.session.commit()

    return redirect('/books')

# ----- MAGAZINES -----
@library.route('/magazines', methods=['GET', 'POST'])
def magazines():
    if request.method == 'POST':
        title = request.form['title']
        issue = request.form['issue']
        publisher = request.form['publisher']
        year = int(request.form['year'])

        last_rank = db.session.query(db.func.max(Magazine.rank)).scalar()
        new_rank = (last_rank or 0) + 1

        new_magazine = Magazine(title=title, issue=issue, publisher=publisher, year=year, rank=new_rank)
        db.session.add(new_magazine)
        db.session.commit()
        return redirect('/magazines')

    search_q = request.args.get('search', '').strip()
    query = Magazine.query
    if search_q:
        query = query.filter(
            (Magazine.title.ilike(f"%{search_q}%")) |
            (Magazine.publisher.ilike(f"%{search_q}%")) |
            (Magazine.year.like(search_q))
        )

    magazines = query.order_by(Magazine.rank).all()

    matched_ranks = [b.rank for b in magazines]
    if matched_ranks:
        message = f" Magazines with rank : {', '.join(map(str, matched_ranks))}"
    else:
        message = ("Nothing found")
        
    return render_template(
        'index.html',
        mode="magazines",
        items=magazines,
        message=message,
        search_mode=bool(search_q))

@library.route('/delete_magazine/<int:id>')
def delete_magazine(id):
    magazine = Magazine.query.get_or_404(id)
    db.session.delete(magazine)
    db.session.commit()

    magazines = Magazine.query.order_by(Magazine.rank).all()
    for i, m in enumerate(magazines, start=1):
        m.rank = i
    db.session.commit()

    return redirect('/magazines')

# ----- FILMS -----
@library.route('/films', methods=['GET', 'POST'])
def films():
    if request.method == 'POST':
        title = request.form['title']
        director = request.form['director']
        year = int(request.form['year'])
        genre = request.form['genre']

        last_rank = db.session.query(db.func.max(Film.rank)).scalar()
        new_rank = (last_rank or 0) + 1

        new_film = Film(title=title, director=director, year=year, genre=genre, rank=new_rank)
        db.session.add(new_film)
        db.session.commit()
        return redirect('/films')

    query = Film.query
    if search_q:
        query = query.filter(
            (Film.title.ilike(f"%{search_q}%")) |
            (Film.director.ilike(f"%{search_q}%")) |
            (Film.year.like(search_q))
        )

    films = query.order_by(Film.rank).all()

    matched_ranks = [b.rank for b in films]
    if matched_ranks:
        message = f" Films with rank : {', '.join(map(str, matched_ranks))}"
    else:
        message = ("Nothing found")
        
    return render_template(
        'index.html',
        mode="films",
        items=films,
        message=message,
        search_mode=bool(search_q))

@library.route('/delete_film/<int:id>')
def delete_film(id):
    film = Film.query.get_or_404(id)
    db.session.delete(film)
    db.session.commit()

    films = Film.query.order_by(Film.rank).all()
    for i, f in enumerate(films, start=1):
        f.rank = i
    db.session.commit()

    return redirect('/films')

# ---------- INIT ----------
if __name__ == '__main__':
    with library.app_context():
        db.create_all()    
    library.run(debug=True)