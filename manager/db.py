import datetime
import random
import sqlite3

import click 
from flask import current_app, g
from flask.cli import with_appcontext

from . import lister

def get_db():
    if 'db' not in g: 
        dbname = current_app.config['DATABASE'] 
        g.db = sqlite3.connect(dbname)
        g.db.execute("PRAGMA foreign_keys = ON;")
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    
    f = current_app.open_resource("sql/create.sql")
    sql_code = f.read().decode("ascii")
    cur = db.cursor()
    cur.executescript(sql_code)
    cur.close()
    db.commit()

    cur = db.cursor()
    date = datetime.datetime.today()
    day = lister.get_date(date)
    time = lister.get_time(date)
    title = "Exam"
    Description = "Remind me to take the exam at 3 pm on today"
    done = 0
    cur.execute("INSERT INTO Tasks (task_date, task_time, Title, Description, done) VALUES (?,?,?,?,?)",[day, time, title, Description, done])
    desc2 = "so cool to do it"
    done2 = 1
    cur.execute("INSERT INTO Tasks (task_date, task_time, Title, Description, done) VALUES (?,?,?,?,?)",[day, time, title, desc2, done2])


    click.echo("Insertions done")
    cur.close()
    db.commit()
    close_db()




@click.command('initdb', help="initialise the database")
@with_appcontext
def init_db_command():
    init_db()
    click.echo('DB initialised') 

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)