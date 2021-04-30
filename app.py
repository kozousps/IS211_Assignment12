from flask import (Flask, render_template, redirect,
                   session, url_for, request, g)
from markupsafe import escape
# from db import get_db
# import os
import sqlite3


app = Flask(__name__)
# dbhere = os.path.join(app.instance_path, 'hw13.db')
# Configure app, and displays database path
app.config.from_mapping(
    SECRET_KEY='ultrastrongkey',
    # DATABASE=dbhere
    )


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('hw13.db')
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close


@app.before_request
def before_request():
    g.db = get_db()


# Initializes and gets db
with app.app_context():
    db = get_db()


@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as {}'.format(escape(session['username']))
    return '''You are not logged in.
        <p><a href="login">Login</a></p>
        '''


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':
            return redirect(url_for('dashboard'))
        else:
            logout()
            return redirect(url_for('login'))
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/dashboard', methods=['GET'])
def dashboard():
    if session['username'] == 'admin':
        if request.method == 'GET':
            studret = g.db.execute("SELECT * FROM students").fetchall()
            quizret = g.db.execute("SELECT * FROM quizzes").fetchall()

            students = [
                        dict(First=r[0],
                             Last=r[0],
                             Studentid=r[0]) for r in studret
                        ]
            # quizzes = [
            #            dict(quizid=quizret[0],
            #                 subject=quizret[1],
            #                 qs=quizret[2],
            #                 date=quizret[3])
            #            ]

            return render_template('dashboard.html', students=students,
                                   quizzes=quizret)
    return redirect(url_for('index'))


@app.route('/student/add', methods=['POST'])
def studentadd():
    if session['username'] == 'admin':
        pass


if __name__ == '__main__':
    app.run(debug=True)
