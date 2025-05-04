from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html', title="Books")


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
