import datetime

from flask import Blueprint
from flask import render_template, request, redirect, url_for, jsonify
from flask import g

from . import db

bp = Blueprint("lister", "lister", url_prefix="")

months = {1:"Jan", 2:"Feb", 3:"March", 5:"May", 4:"April", 6:"June", 7:"July", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}
weekday = {1:"Mon", 2:"Tue", 3:"Wed", 4:"Thu", 5:"Fri", 6:"Sat", 7:"Sun"}

def get_date(d):
    d = str(d)
    d = datetime.datetime.strptime(d, '%Y-%m-%d')
    return d.date()

def get_time(d):
    d = str(d)
    d = datetime.datetime.strptime(d, '%H:%M')
    time = d.strftime("%H: %M")
    return time

def format_date(d):
    if d:
        d = datetime.datetime.strptime(d, '%Y-%m-%d')
        v = d.strftime("%a - %b %d, %Y")
        return v
    else:
        return None

def get_weekday(d):
    day_of_week = weekday[get_date(d).isocalendar()[2]]
    return day_of_week

def display_date(d):
    date = str(d)
    day = date[8:]
    month = months[int(date[5:7])]
    weekday = get_weekday(d)
    notation = {1:"st", 2:"nd", 3:"rd", 21:"st", 22:"nd", 23:"rd", 31:"st"}
    add = "th"
    if(int(day) in notation.keys()):
        add = notation[int(day)]

    final =  str(int(day)) + add +" " + month + " " + "( " + weekday + " )"
    return final



@bp.route("/")
def home_page():
    conn = db.get_db()
    cur = conn.cursor()
    '''cur.execute("SELECT id, task_date, task_time, Title, Description FROM Tasks WHERE Done = ?",[0])
    id, day, time, title, description = cur.fetchall()[0]
    print("They are: ")
    print(id, day, time,  title, description)
    '''
    cur.execute("SELECT id, task_date, task_time, Title, Description FROM Tasks WHERE Done = ?",[0])
    today = datetime.datetime.today().date()
    
    values = cur.fetchall()
    print("And values are: ")
    print(values)
    values = list(filter(lambda x: get_date(x[1]) <= get_date(today) , values))
    print("new values after filter are: ")
    print(values)
    cur.close()
    conn.commit()
    db.close_db()
    for i in range(len(values)):
        templ = list(values[i])
        templ.append("day")
        templ[1] = display_date(templ[1])
        values[i] = templ

    print("new values after week are: ", values)
    return render_template('home_page.html', values = values, heading = "Alerts/Overdues")

@bp.route("/add_task", methods=["GET", "POST"])
def AddTask():
    conn = db.get_db()
    cursor = conn.cursor()
    if request.method == "GET":      
        return render_template("add_task.html")

    elif request.method == "POST":
        description = request.form.get('Description').lstrip().rstrip()
        Title = request.form.get('Title').lstrip().rstrip()
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
    cur.execute("SELECT id, task_date, task_time, Title, Description FROM Tasks WHERE Done = ? AND task_date = ?",[0, today_date])
    values = cur.fetchall()
    print("And values are: ")
    print(values)

    cur.close()
    conn.commit()
    db.close_db()
    for i in range(len(values)):
        templ = list(values[i])
        templ.append("day")
        templ[1] = display_date(templ[1])
        values[i] = templ

    return render_template('home_page.html', values = values, heading = "Tasks to be done today")


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
    print('rest of the week is ', rest_of_week)
    cur.execute("SELECT id, task_date, task_time, Title, Description FROM Tasks WHERE Done = ? ",[0,])
    values = cur.fetchall()
    print("weeks values are : ", values)
    values = list(filter(lambda x: x[1] in rest_of_week, values))
    print("final values are : ", values)
    cur.close()
    conn.commit()
    db.close_db()
    for i in range(len(values)):
        templ = list(values[i])
        templ.append("day")
        templ[1] = display_date(templ[1])
        values[i] = templ


    return render_template('home_page.html', values = values, heading = "Tasks for the Week")

@bp.route("/<id>/edit_task", methods=["GET", "POST"])
def Edit_tasks(id):
    conn = db.get_db()
    cursor = conn.cursor()
    values = cursor.execute("SELECT id, Title, Description, original_task_time FROM Tasks WHERE id = ? ",[id,])
    values = cursor.fetchall()
    date_goog_init = cursor.execute("SELECT original_task_time FROM Tasks WHERE id = ?", [id]).fetchall()[0]
    print("inti google date is: ", date_goog_init)
    if request.method == "GET":
        #('foo')
        return render_template("edit_task.html", values = values)

    elif request.method == "POST":
        description = request.form.get('Description').lstrip().rstrip()
        Title = request.form.get('Title').lstrip().rstrip()
        # done = 0
        date_goog = request.form.get('birthdaytime')
        print("received date_goog is ", date_goog)
        if(date_goog is None) or len(date_goog) < 2:
            date_goog = date_goog_init[0]
        #date_goog = date_goog_init[0]
        date = get_date(date_goog[:10])
        time = get_time(date_goog[11:])
        cursor.execute("UPDATE Tasks SET description = ?, Title = ?, task_date = ?, task_time = ?, original_task_time=? WHERE id = ?",[description, Title, date, time, date_goog, id])
        print("These inserted")
        cursor.close()
        conn.commit()
        db.close_db()
        
        return redirect(url_for("lister.home_page"))


@bp.route("/<id>/done_task", methods=["GET", "POST"])
def Done_tasks(id):
    conn = db.get_db()
    cursor = conn.cursor()
    if request.method == "GET":      
        #return render_template("base.html")
        page_curr = request.form.get('pages')
        cursor.execute("UPDATE TASKS SET Done = ? where id = ?",[1, id])
        cursor.close()
        conn.commit()
        db.close_db()
        if(page_curr == "week"):
            return redirect(url_for("lister.Week_tasks"))
        
        else:
            return redirect(url_for("lister.Today_tasks"))

    else:
        page_curr = request.form.get('pages')
        cursor.execute("UPDATE TASKS SET Done = ? where id = ?",[1, id])
        cursor.close()
        conn.commit()
        db.close_db()
        if(page_curr == "week"):
            return redirect(url_for("lister.Week_tasks"))
        
        else:
            return redirect(url_for("lister.Today_tasks"))

@bp.route("/history")
def history():
    conn = db.get_db()
    cursor = conn.cursor()    



