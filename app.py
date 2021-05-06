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
        return """Logged in as {}
               <p><a href="dashboard">Dashboard</a></p>
               """.format(escape(session['username']))
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

            # studlist = [
            #             dict(First=r['firstname'],
            #                  Last=r['lastname'],
            #                  Studentid=r['id']) for r in studret
            #             ]
            # quizzes = [
            #            dict(quizid=quizret[0],
            #                 subject=quizret[1],
            #                 qs=quizret[2],
            #                 date=quizret[3])
            #            ]

            return render_template('dashboard.html', students=studret,
                                   quizzes=quizret)
    return redirect(url_for('index'))


@app.route('/student/add', methods=['GET', 'POST'])
def studentadd():
    if session['username'] == 'admin':
        if request.method == 'GET':
            return render_template('studentadd.html')
        if request.method == 'POST':
            try:
                addstu = (request.form["fname"], request.form['lname'])
                g.db.execute("""INSERT INTO students (firstname, lastname)
                             VALUES (?, ?);""", (addstu),
                             )
                g.db.commit()
                return redirect(url_for('dashboard'))
            except Exception as e:
                print(e)
                return render_template('studentadd.html')


@app.route('/quiz/add', methods=['GET', 'POST'])
def quizadd():
    if session['username'] == 'admin':
        if request.method == 'GET':
            return render_template('quizadd.html')
        if request.method == 'POST':
            try:
                addqui = (request.form["subject"], request.form['qs'],
                          request.form['date'])
                g.db.execute("""INSERT INTO quizzes (subject, qs, date)
                             VALUES (?, ?, ?);""", (addqui),
                             )
                g.db.commit()
                return redirect(url_for('dashboard'))
            except Exception as e:
                print(e)
                return render_template('quizadd.html')


@app.route('/student/<id>')
def quizscore(id):
    qscr = g.db.execute("""
                        SELECT quizzes.id, student_result.grade, quizzes.date
                        FROM students JOIN student_result ON students.id =
                        student_result.studentid
                        JOIN quizzes ON student_result.quizid = quizzes.id
                        WHERE students.id = ?
                        """, [id]).fetchall()

    return render_template('studentscore.html', qscr=qscr)


@app.route('/result/add', methods=['GET', 'POST'])
def resultadd():
    if session['username'] == 'admin':
        if request.method == 'GET':
            return render_template('resultadd.html')
        if request.method == 'POST':
            try:
                resultqui = (request.form["studentid"], request.form['quizid'],
                             request.form['grade'])
                g.db.execute("""
                             INSERT INTO student_result
                             (studentid, quizid, grade)
                             VALUES (?, ?, ?);""", (resultqui),
                             )
                g.db.commit()
                return redirect(url_for('dashboard'))
            except Exception as e:
                print(e)
                return render_template('resultadd.html')


if __name__ == '__main__':
    app.run(debug=True)
