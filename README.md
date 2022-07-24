# Todo List Manager
To do list manager is web application that helps in remainding your tasks, alerts your overdues, and gives you a list of daily and weekly tasks to be done.
This app is mainly intended to run with python version > python 3.6 and ubuntu version > ubuntu 18. Please ensure that you have these criteria fulfilled to run the web app.

* Run the commands on the terminal to install git to clone the repository 
1) ```sudo apt-get update```
2) ```sudo apt-get install git```

* Clone the repository using the command 
```git clone https://github.com/Tanuj2552/Todo-List-Manager.git```

* Run this command to install all the modules required (you can run this in virtul env if you want, refer - https://linuxize.com/post/how-to-create-python-virtual-environments-on-ubuntu-18-04/)
```pip install -r requirements.txt```

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

