import datetime

from flask import Blueprint
from flask import render_template, request, redirect, url_for, jsonify
from flask import g

from . import db

bp = Blueprint("lister", "lister", url_prefix="")

def get_date(d):
    return d.date()

def get_time(d):
    time = d.strftime("%H: %M")
    return time

@bp.route("/")
def dashboard():
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("SELECT task_date, task_time, Title, Description FROM Tasks WHERE Done = ?",[0])
    day, time, title, description = cur.fetchall()[0]
    print("They are: ")
    print(day, time,  title, description)
    cur.execute("SELECT task_date, task_time, Title, Description FROM Tasks WHERE Done = ?",[0])
    values = cur.fetchall()
    print("And values are: ")
    print(values)

    return render_template('index.html', values = values)

@bp.route("/homepage")
def home_page():
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("SELECT task_date, task_time, Title, Description FROM Tasks WHERE Done = ?",[0])
    day, time, title, description = cur.fetchall()[0]
    print("They are: ")
    print(day, time,  title, description)
    cur.execute("SELECT task_date, task_time, Title, Description FROM Tasks WHERE Done = ?",[0])
    values = cur.fetchall()
    print("And values are: ")
    print(values)

    cur.close()
    conn.commit()
    db.close_db()

    return render_template('index.html', values = values)

@bp.route("/add_task", methods=["GET", "POST"])
def AddTask():
    conn = db.get_db()
    cursor = conn.cursor()
    if request.method == "GET":
      
        return render_template("add_task.html")

    elif request.method == "POST":
        description = request.form.get('Description')
        Title = request.form.get('Title')
        done = 0
        cursor.execute("INSERT INTO Tasks (Title, Description, Done) VALUES (?,?,?)",[Title, description, done])
        print("These inserted")
        cursor.close()
        conn.commit()
        db.close_db()


        # TODO Handle sold
        return redirect(url_for("lister.home_page"))