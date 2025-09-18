from flask import Flask, render_template, request
import sqlite3

# Initialize Flask app
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
                -- GROUP_CONCAT to combine multiple genres for each book
                -- into one value, separated by comma and space
        SELECT books.id, books.name, books.photo, books.year_published,
             books.rating, GROUP_CONCAT(genre.name, ', ') AS genres
        FROM books
                -- Join books and books_genre tables on book id
        JOIN books_genre ON books.id = books_genre.book_id
                -- Join books_genre and genre tables on genre id
        JOIN genre ON books_genre.genre_id = genre.id
                -- Combine rows with same book id into one row,
                -- so each book id only has one row,
                -- complementary to GROUP_CONCAT
        GROUP BY books.id
                -- Order the books alphabetically by name
        ORDER BY books.name;
    ''')
    books = cur.fetchall()  # Fetch all results from query
    # Render books html, pass title, books and genres as variables for jinja -
    # to use
    # books on the right is the results from the query,
    # books on the left is the variable
    return render_template("books.html", title="Books", books=books)


# Route for individual book page
@app.route('/books/<int:id>')
def book_by_id(id):
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute('''
                -- GROUP_CONCAT to combine multiple genres for each book with
                -- their id seperated by colon and each genre/id seperated by
                -- comma and space
        SELECT books.id, books.name, books.photo, books.year_published,
            books.rating, books.description, author.name, author.id,
            GROUP_CONCAT(genre.name || ':' || genre.id, ', ') AS genres
        FROM books
                -- Join id in books table with book_id in books_genre table
        JOIN books_genre ON books.id = books_genre.book_id
                -- Join genre_id in books_genre table with id in genre table
        JOIN genre ON books_genre.genre_id = genre.id
                -- Join author_id in books table with id in author table
        JOIN author ON books.author_id = author.id
                -- ? is a placeholder for the id parameter
        WHERE books.id = ?
                -- Combine rows with same book id into one row,
                -- so each book id only has one row,
                -- complementary to GROUP_CONCAT
        GROUP BY books.id;
    ''', (id,))
    # Fetch the one result from query(the one with the matching id)
    book = cur.fetchone()
    conn.close()
    # If no book with that id, return 404 page
    if book is None:
        return render_template("404.html", title="404 Not Found"), 404
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
    # If no author with that id, return 404 page
    if author is None:
        return render_template("404.html", title="404 Not Found"), 404
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
    cur.execute('SELECT id, name FROM genre ORDER BY name')
    genres = cur.fetchall()  # Fetch all results from query
    conn.close()
    # Render genres html, pass title and genres as variables for jinja to use
    # genres on the right is the results from the query,
    # genres on the left is the variable
    return render_template("genres.html", title="Genres", genres=genres)


# Route for individual genre page
@app.route('/genres/<int:id>')
def genre_by_id(id):
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    # Select from genre table
    cur.execute('SELECT id, name, description FROM genre WHERE id = ?', (id,))
    # Fetch the one result from query(the one with the matching id)
    genre = cur.fetchone()
    # If no genre with that id, return 404 page
    if genre is None:
        conn.close()
        return render_template("404.html", title="404 Not Found"), 404
    cur.execute('''
                -- GROUP_CONCAT to combine multiple genres for each book
                -- into one value, separated by comma and space
        SELECT books.id, books.name, books.photo, books.year_published,
             books.rating, GROUP_CONCAT(genre.name, ', ') AS genres
        FROM books
                -- Join books and books_genre tables on book id
        JOIN books_genre ON books.id = books_genre.book_id
                -- Join books_genre and genre tables on genre id
        JOIN genre ON books_genre.genre_id = genre.id
                -- Fetches only the books that have the genre id matching the
                -- id parameter
        WHERE books.id IN (
            SELECT book_id FROM books_genre WHERE genre_id = ?
        )
                -- Combine rows with same book id into one row,
                -- so each book id only has one row,
                -- complementary to GROUP_CONCAT
        GROUP BY books.id
                -- Order the books alphabetically by name
        ORDER BY books.name;
    ''', (id,))
    books = cur.fetchall()  # Fetch all results from query
    conn.close()
    # Render all_genres html, pass id, genre and books as variables for jinja -
    # to use
    # genre/books on the right is the result from the query,
    # genre/books on the left is the variable
    return render_template("all_genres.html", genre=genre, books=books)


# 404 error handler, for page not found errors
@app.errorhandler(404)
def page_not_found(e):
    # Return 404 HTTP status code
    return render_template("404.html", title="404 Not Found"), 404


# 500 error handler, for internal server errors
@app.errorhandler(500)
def internal_server_error(e):
    # Return 500 HTTP status code
    return render_template("500.html", title="500 Internal Server Error"), 500


# Broader exception handler for any uncaught errors(dealed as 500 errors)
@app.errorhandler(Exception)
def handle_exception(e):
    # Return 500 HTTP status code
    return render_template("500.html", title="500 Internal Server Error"), 500


# Route for search page
@app.route('/search')
def search():
    # Get the search input from the url parameter
    query = request.args.get('query')
    # maximum length of input is 40 characters, anything longer is treated
    # as a potential attack and returns 500 error page
    MAX_LENGTH = 40
    if len(query) > MAX_LENGTH:
        return (
            render_template("500.html", title="500 Internal Server Error"), 500
        )
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    # Search books
    cur.execute('''
                -- GROUP_CONCAT to combine multiple genres for each book
                -- into one value, separated by comma and space
        SELECT books.id, books.name, books.photo, books.year_published,
             books.rating, GROUP_CONCAT(genre.name, ', ') AS genres
        FROM books
                -- Join books and books_genre tables on book id
        JOIN books_genre ON books.id = books_genre.book_id
                -- Join books_genre and genre tables on genre id
        JOIN genre ON books_genre.genre_id = genre.id
                -- LIKE ? compares data to the input
                -- CAST(... AS TEXT) converts integers to strings for LIKE to
                -- work
        WHERE books.name LIKE ? OR CAST(books.year_published AS TEXT) LIKE ?
                -- Combine rows with same book id into one row,
                -- so each book id only has one row,
                -- complementary to GROUP_CONCAT
        GROUP BY books.id
                -- Order the books alphabetically by name
        ORDER BY books.name;
                -- f"%{query}%" ensures the input is a string, % is a wildcard
                -- placed in the front and back, it will match anything that
                -- contains the input
    ''', (f"%{query}%", f"%{query}%"))
    books = cur.fetchall()  # Fetch all results from query
    # Search authors
    cur.execute('''
        SELECT id, name, birth_year, nationality, photo, biography
        FROM author
                -- LIKE ? compares data to the input
        WHERE author.name LIKE ? OR CAST(author.birth_year AS TEXT) LIKE ?
                -- Order by name alphabetically
        ORDER BY name;
                -- f"%{query}%" ensures the input is a string, % is a wildcard
                -- placed in the front and back, it will match anything that
                -- contains the input
    ''', (f"%{query}%", f"%{query}%"))
    authors = cur.fetchall()  # Fetch all results from query
    # Search genres
    cur.execute('''
        SELECT id, name, description
        FROM genre
                -- LIKE ? compares data to the input
        WHERE genre.name LIKE ? OR genre.description LIKE ?
                -- Order by name alphabetically
        ORDER BY name
                -- f"%{query}%" ensures the input is a string, % is a wildcard
                -- placed in the front and back, it will match anything that
                -- contains the input
    ''', (f"%{query}%", f"%{query}%"))
    genres = cur.fetchall()  # Fetch all results from query
    conn.close()
    # Render search html, pass title, books, authors, genres and query as
    # variables for jinja to use
    # books/authors/genres on the right is the results from the query,
    # books/authors/genres on the left is the variable
    return render_template("search.html", title="Search Results", books=books,
                           authors=authors, genres=genres, query=query)


# Run the app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
