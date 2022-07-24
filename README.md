# Todo List Manager
To do list manager is web application that helps in remainding your tasks, alerts your overdues, and gives you a list of daily and weekly tasks to be done.

* Please run the following commands on the terminal to create database for the web app
```sudo apt update```
1) ```sudo apt install sqlite3``` - to install sqlite3
2) ```sqlite3 DATABASE.db``` - to create database

* Please run the following commands on the terminal after cloning the repository to setup the web app
1) ```export FLASK_ENV=development```
2) ```export FLASK_APP=manager```

* And after setting the flask app run these commands on the terminal to set up the database and to run the application
1) ```flask initdb``` - to setup the database for the web application
2) ```flask run``` - to run the web application

