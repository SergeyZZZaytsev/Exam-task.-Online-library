from flask import Flask,render_template, url_for
from flask_sqlalchemy import SQLAlchemy

library = Flask(__name__)
library.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db = SQLAlchemy(library)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'

@library.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    library.run(debug=True)