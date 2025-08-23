from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route('/')
def home():
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute('''
        SELECT id, name, photo, rating
        FROM books
        ORDER BY rating DESC
        LIMIT 10;
    ''')
    books = cur.fetchall()
    conn.close()
    return render_template("home.html", title="My Book Library", books=books)


@app.route('/books')
def books():
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute('''
        SELECT books.id, books.name, books.photo, books.year_published,
             books.rating, genre.name
        FROM books
        JOIN genre ON books.genre_id = genre.id
        ORDER BY genre.name, books.name;
    ''')
    books = cur.fetchall()
    cur.execute('''
        SELECT * FROM genre ORDER by name''')
    genres = cur.fetchall()
    conn.close()
    return render_template("books.html", title='Books', books=books,
                           genres=genres)


@app.route('/books/<int:id>')
def book_by_id(id):
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute('''
        SELECT books.id, books.name, books.photo, books.year_published,
            books.rating, books.description, genre.name, author.name
        FROM books
        JOIN genre ON books.genre_id = genre.id
        JOIN author ON books.author_id = author.id
        WHERE books.id = ?;
    ''', (id,))
    book = cur.fetchone()
    conn.close()
    return render_template("all_books.html", id=id, book=book)


@app.route('/authors')
def authors():
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute('''
        SELECT id, name, birth_year, nationality, photo, biography
        FROM author
        ORDER BY name;
    ''')
    authors = cur.fetchall()
    conn.close()
    return render_template("authors.html", title="Authors", authors=authors)


@app.route('/genres')
def genres():
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute('SELECT id, name, description FROM genre ORDER BY name')
    genres = cur.fetchall()
    conn.close()
    return render_template("genres.html", title='Genres', genres=genres)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.route('/pet_rocks/<int:id>')
def pet_rocks(id):
    return render_template('pet_rocks.html', id=id)


@app.route('/all_pizzas')
def all_pizzas():
    conn = sqlite3.connect('flask/pizza.db')
    cur = conn.cursor()
    cur.execute('SELECT * from Pizza')  # select id,name
    pizzas = cur.fetchall()  # all = list(none), one = a thing(none will break)
    conn.close()
    return render_template('all_pizzas.html', pizzas=pizzas)


@app.route('/all_pizzas/<int:id>')
def pizza_by_id(id):
    conn = sqlite3.connect('flask/pizza.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM pizza WHERE id = ?', (id,))
    pizza = cur.fetchone()
    conn.close()
    return render_template('pizza.html', pizza=pizza)


if __name__ == '__main__':
    app.run(debug=True)
