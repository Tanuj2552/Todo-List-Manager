from flask import Flask, render_template

app = Flask("manager")

@app.route('/')
def start():
    return render_template("index.html")
