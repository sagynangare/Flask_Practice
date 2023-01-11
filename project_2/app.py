#app.py
from flask import Flask, render_template, request, redirect, url_for, flash

#import psycopg2 #pip install psycopg2 
#import psycopg2.extras

import sqlite3

app = Flask(__name__)

app.secret_key = "cairocoders-ednalan"
 
# DB_HOST = "localhost"
# DB_NAME = "sampledb"
# DB_USER = "postgres"
# DB_PASS = "admin"
 
#conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

conn=sqlite3.connect("searching.db", check_same_thread=False)

cur=conn.cursor()

#cur.execute("CREATE TABLE students (id INTEGER PRIMARY KEY AUTOINCREMENT, fname text NOT NULL, lname text NOT NULL, email text NOT NULL)")

@app.route('/')
def Index():
    #cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM students"
    cur.execute(s) # Execute the SQL
    list_users = cur.fetchall()

    return render_template('index.html', list_users = list_users)
 
@app.route('/add_student', methods=['POST'])
def add_student():
    #cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        cur.execute("INSERT INTO students (fname, lname, email) VALUES (?,?,?)", (fname, lname, email))
        conn.commit()
        flash('Student Added successfully')
        return redirect(url_for('Index'))
 
@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_employee(id):
    #cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute('SELECT * FROM students WHERE id = ?', (id,))
    data = cur.fetchall()
    #cur.close()
    print(data[0][0])
    return render_template('edit.html', student = data)
 
@app.route('/update/<id>', methods=['POST'])
def update_student(id):
    print("Employee id=",id)
    if request.method == 'POST':
        print(request.method=='POST')
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']

        print(f"fname: {fname}\nLname:{lname}\nemail:{email}")
        #cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            UPDATE students
            SET fname = ?,
                lname = ?,
                email = ?
            WHERE id = ?
        """, (fname, lname, email, id))
        flash('Student Updated Successfully')
        conn.commit()
        return redirect(url_for('Index'))
 
@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_student(id):
    #cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute('DELETE FROM students WHERE id = {0}'.format(id))
    conn.commit()
    flash('Student Removed Successfully')
    return redirect(url_for('Index'))
 
if __name__ == "__main__":
    app.run(debug=True)
