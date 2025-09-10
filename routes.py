from flask import Flask, render_template, request
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
    return render_template("books.html", title="Books", books=books,
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
    return render_template("genres.html", title="Genres", genres=genres)


# 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", title="404 Not Found"), 404
# Return 404 HTTP status code


@app.route('/search')
def search():
    # Get the search input from the url parameter
    query = request.args.get('query')
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    # Search books
    cur.execute('''
        SELECT books.id, books.name, books.photo, books.year_published,
             books.rating, genre.name
        FROM books
        JOIN genre ON books.genre_id = genre.id
        WHERE books.name LIKE ? OR CAST(books.year_published AS TEXT) LIKE ?
        ORDER BY genre.name, books.name;
    ''', (f"%{query}%", f"%{query}%"))
    books = cur.fetchall()
    # Search authors
    cur.execute('''
        SELECT id, name, birth_year, nationality, photo, biography
        FROM author
        WHERE author.name LIKE ? OR CAST(author.birth_year AS TEXT) LIKE ?
        ORDER BY name;
    ''', (f"%{query}%", f"%{query}%"))
    authors = cur.fetchall()
    # Search genres
    cur.execute('''
    SELECT id, name, description
    FROM genre
    WHERE genre.name LIKE ? OR genre.description LIKE ?
    ORDER BY name
    ''', (f"%{query}%", f"%{query}%"))
    genres = cur.fetchall()
    # LIKE ? compares data to the input, f"%{query}%" ensures the input is a
    # string, % in the front and back will match anything that contains the
    # input, CAST(... AS TEXT) converts integers to strings for LIKE to work
    conn.close()
    return render_template("search.html", title="Search Results", books=books,
                           authors=authors, genres=genres, query=query)


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
