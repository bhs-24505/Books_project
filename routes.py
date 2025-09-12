from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


# Route for the home page
@app.route('/')
def home():
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute('''
                -- Select 10 highest rated books
        SELECT id, name, photo, rating
        FROM books
                -- From highest rating to lowest
        ORDER BY rating DESC
        LIMIT 10;
    ''')
    books = cur.fetchall()  # Fetch all results from query
    conn.close()
    # Render home html, pass title and books as variables for jinja to use
    # books on the right is the results from the query,
    # books on the left is the variable
    return render_template("home.html", title="My Book Library", books=books)


# Route for the books page
@app.route('/books')
def books():
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute('''
                -- Select from books and genre tables
        SELECT books.id, books.name, books.photo, books.year_published,
             books.rating, genre.name
        FROM books
                -- Join genre_id in books table with id in genre table
        JOIN genre ON books.genre_id = genre.id
                -- Order by genre name, then book name alphabetically
        ORDER BY genre.name, books.name;
    ''')
    books = cur.fetchall()  # Fetch all results from query
    # Get name from genre table ordered by name alphabetically
    cur.execute('''
        SELECT name FROM genre ORDER by name''')
    genres = cur.fetchall()  # Fetch all results from query
    conn.close()
    # Render books html, pass title, books and genres as variables for jinja -
    # to use
    # books/genres on the right is the results from the query,
    # books/genres on the left is the variable
    return render_template("books.html", title="Books", books=books,
                           genres=genres)


# Route for individual book page
@app.route('/books/<int:id>')
def book_by_id(id):
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute('''
                -- Select from books, genre and author tables
        SELECT books.id, books.name, books.photo, books.year_published,
            books.rating, books.description, genre.name, author.name
        FROM books
                -- Join genre_id in books table with id in genre table
        JOIN genre ON books.genre_id = genre.id
                -- Join author_id in books table with id in author table
        JOIN author ON books.author_id = author.id
                -- ? is a placeholder for the id parameter
        WHERE books.id = ?;
    ''', (id,))
    # Fetch the one result from query(the one with the matching id)
    book = cur.fetchone()
    conn.close()
    # Render all_books html, pass id and book as variables for jinja to use
    # book on the right is the result from the query,
    # book on the left is the variable
    return render_template("all_books.html", id=id, book=book)


# Route for the authors page
@app.route('/authors')
def authors():
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute('''
                -- Select from author table
        SELECT id, name, birth_year, nationality, photo
        FROM author
                -- Order by name alphabetically
        ORDER BY name;
    ''')
    authors = cur.fetchall()  # Fetch all results from query
    conn.close()
    # Render authors html, pass title and authors as variables for jinja to use
    # authors on the right is the results from the query,
    # authors on the left is the variable
    return render_template("authors.html", title="Authors", authors=authors)


# Route for individual author page
@app.route('/authors/<int:id>')
def author_by_id(id):
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute('''
                -- Select from author table
        SELECT id, name, birth_year, nationality, photo, biography
        FROM author
                -- ? is a placeholder for the id parameter
        WHERE id = ?;
    ''', (id,))
    # Fetch the one result from query(the one with the matching id)
    author = cur.fetchone()
    conn.close()
    # Render all_authors html, pass id and author as variables for jinja to use
    # author on the right is the result from the query,
    # author on the left is the variable
    return render_template("all_authors.html", id=id, author=author)


# Route for genres page
@app.route('/genres')
def genres():
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    # Select from genre table ordered by name alphabetically
    cur.execute('SELECT id, name, description FROM genre ORDER BY name')
    genres = cur.fetchall()  # Fetch all results from query
    conn.close()
    # Render genres html, pass title and genres as variables for jinja to use
    # genres on the right is the results from the query,
    # genres on the left is the variable
    return render_template("genres.html", title="Genres", genres=genres)


# 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    # Return 404 HTTP status code
    return render_template("404.html", title="404 Not Found"), 404


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
