import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def render_index():
    return render_template("loginform.html")



con = sqlite3.connect('place.db')
cur = con.cursor()


cur.execute("""CREATE TABLE company(
    company_id text PRIMARY KEY,
    company name text,
    total_students_place,
    max_package,
    avg_package
    )
    """)

cur.execute("""CREATE TABLE questions(
    q_id integer PRIMARY KEY,
    question text,
    dif_level text,
    year text,
    no_of_times text,
    company_id text,
    FOREIGN KEY (company_id) REFERENCES company (company_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
    )
    """)

cur.execute("""CREATE TABLE student(
    ssn text PRIMARY KEY,
    name text,
    age text,
    gender text,
    college text
    )
    """)

cur.execute("""CREATE TABLE answers(
    ans_id text PRIMARY KEY,
    solution text,
    q_id text,
    FOREIGN KEY (q_id) REFERENCES questions (q_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
    )
    """)

cur.execute("""CREATE TABLE feedback(
    f_id text PRIMARY KEY,
    feedback text,
    ssn text,
    FOREIGN KEY(ssn) REFERENCES student (ssn)
    ON DELETE CASCADE
    ON UPDATE CASCADE
    )
    """)


