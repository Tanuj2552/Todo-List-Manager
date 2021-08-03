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

def get_date(d):
    return d.date()

def get_time(d):
    time = d.strftime("%H: %M")
    return time

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
    day = get_date(date)
    time = get_time(date)
    title = "subscribe"
    Description = "Please subscribe to get preimum features"
    done = 0
    cur.execute("INSERT INTO Tasks (task_date, task_time, Title, Description, done, original_task_time) VALUES (?,?,?,?,?,?)",[day, time, title, Description, done, date])
    '''
    desc2 = "so cool to do it"
    done2 = 1
    cur.execute("INSERT INTO Tasks (task_date, task_time, Title, Description, done, original_task_time) VALUES (?,?,?,?,?,?)",[day, time, title, desc2, done2, date])
    '''
    
    click.echo("Insertions done")
    close_db()


@click.command('initdb', help="initialise the database")
@with_appcontext
def init_db_command():
    init_db()
    click.echo('DB initialised') 

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)