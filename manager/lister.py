import datetime

from flask import Blueprint
from flask import render_template, request, redirect, url_for, jsonify
from flask import g

from . import db

bp = Blueprint("lister", "lister", url_prefix="")

@bp.route("/")
def dashboard():
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Tasks")
    date, title, description = cur.fetchall()[0]
    print("They are: ")
    print(date, title, description)
    cur.execute("SELECT * FROM Tasks")
    values = cur.fetchall()
    print("And values are: ")
    print(values)

    return render_template('index.html', values = values)