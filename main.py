import os

from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import InputRequired
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-collection.db'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    author = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return f'<Book title: {self.title}>'


with app.app_context():
    db.create_all()


class BookForm(FlaskForm):
    name = StringField('Book Name', validators=[InputRequired()])
    author = StringField('Book Author', validators=[InputRequired()])
    rating = IntegerField()
    submit = SubmitField('Add Book')


@app.route('/')
def home():
    with app.app_context():
        all_books = db.session.query(Book).all()
    return render_template('index.html', books=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_book = Book(
            title=request.form['name'],
            author=request.form['author'],
            rating=request.form['rating']
        )
        with app.app_context():
            db.session.add(new_book)
            db.session.commit()
        return redirect(url_for('home'))

    return render_template('add.html')


@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_rating(book_id):
    book_to_edit = db.session.get(Book, book_id)
    if request.method == 'POST':
        rating = request.form.get('rating')
        book_to_edit.rating = rating
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit_rating.html', book=book_to_edit)


@app.route('/delete/<int:book_id>')
def delete_book(book_id):
    book_to_delete = db.session.get(Book, book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

