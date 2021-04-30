from flask import (Flask, render_template, redirect,
                   session, url_for, request, g)
from markupsafe import escape
import sqlite3
from db import get_db
import os


app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='ultrastrongkey',
    DATABASE=os.path.join(app.instance_path, 'schema.sql'),
    )


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
                        dict(studentid=studret[2],
                             firstn=studret[0],
                             last=studret[1])
                        ]
            quizzes = [
                       dict(quizid=quizret[0],
                            subject=quizret[1],
                            qs=quizret[2],
                            date=quizret[3])
                       ]

            return render_template('dashboard.html', students=students,
                                   quizzes=quizzes)
    return redirect(url_for('index'))


@app.route('/student/add', methods=['POST'])
def studentadd():
    if session['username'] == 'admin':
        pass


if __name__ == '__main__':
    app.run(debug=True)
