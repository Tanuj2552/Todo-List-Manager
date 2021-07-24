import datetime
import random
import sqlite3

import click 
from flask import current_app, g
from flask.cli import with_appcontext

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
    title = "Exam"
    Description = "Remind me to take the exam at 3 pm on today"
    cur.execute("INSERT INTO Tasks (task_date, Title, Description) VALUES (?,?,?)",[date, title, Description])


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