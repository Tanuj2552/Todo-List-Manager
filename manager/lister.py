import datetime

from flask import Blueprint
from flask import render_template, request, redirect, url_for, jsonify
from flask import g

from . import db

bp = Blueprint("lister", "lister", url_prefix="")

def get_date(d):
    d = str(d)
    d = datetime.datetime.strptime(d, '%Y-%m-%d')
    return d.date()

def get_time(d):
    d = str(d)
    d = datetime.datetime.strptime(d, '%H:%M')
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
        date_goog = request.form.get('birthdaytime')
        date = get_date(date_goog[:10])
        time = get_time(date_goog[11:])
        cursor.execute("INSERT INTO Tasks (Title, Description, task_date, task_time, Done, original_task_time) VALUES (?,?,?,?,?,?)",[Title, description, date, time, done, date_goog])
        print("These inserted")
        cursor.close()
        conn.commit()
        db.close_db()

        return redirect(url_for("lister.home_page"))

@bp.route("/todays_tasks")
def Today_tasks():
    conn = db.get_db()
    cur = conn.cursor()
    today_date = str(datetime.datetime.today().date())

    # cur.execute("SELECT task_date, task_time, Title, Description FROM Tasks WHERE Done = ? AND task_date = ?",[0, today_date])
    # day, time, title, description = cur.fetchall()[0]
    # print("They are: ")
    # print(day, time,  title, description)
    cur.execute("SELECT task_date, task_time, Title, Description FROM Tasks WHERE Done = ? AND task_date = ?",[0, today_date])
    values = cur.fetchall()
    print("And values are: ")
    print(values)

    cur.close()
    conn.commit()
    db.close_db()

    return render_template('index.html', values = values)


@bp.route("/weeks_tasks")
def Week_tasks():
    conn = db.get_db()
    cur = conn.cursor()
    today_date = str(datetime.datetime.today().date())

    today = datetime.datetime.today().date()
    dates = [(today + datetime.timedelta(days=i)) for i in range(0 - today.weekday(), 7 - today.weekday())]
    
    dates = [str(get_date(str(datetime.datetime(x.year, x.month, x.day))[:10])) for x in dates]
    
    day_of_week = today.isocalendar()[2] - 1
    rest_of_week = dates[day_of_week:]


    # cur.execute("SELECT task_date, task_time, Title, Description FROM Tasks WHERE Done = ? AND task_date IN (?)",[0, *rest_of_week])
    # day, time, title, description = cur.fetchall()[0]
    # print("They are: ")
    # print(day, time,  title, description)
    cur.execute("SELECT task_date, task_time, Title, Description FROM Tasks WHERE Done = ? AND task_date IN (?)",[0, *rest_of_week])
    values = cur.fetchall()
    # print("And values are: ")
    # print(values)

    cur.close()
    conn.commit()
    db.close_db()

    return render_template('index.html', values = values)