<<<<<<< HEAD

     ,-----.,--.                  ,--. ,---.   ,--.,------.  ,------.
    '  .--./|  | ,---. ,--.,--. ,-|  || o   \  |  ||  .-.  \ |  .---'
    |  |    |  || .-. ||  ||  |' .-. |`..'  |  |  ||  |  \  :|  `--, 
    '  '--'\|  |' '-' ''  ''  '\ `-' | .'  /   |  ||  '--'  /|  `---.
     `-----'`--' `---'  `----'  `---'  `--'    `--'`-------' `------'
    ----------------------------------------------------------------- 


Welcome to your Python project on Cloud9 IDE!

To show what Cloud9 can do, we added a basic sample web application to this
workspace, from the excellent Python tutorial _Learning Python the Hard Way_.
We skipped ahead straight to example 50 which teaches how to build a web
application.

If you've never looked at the tutorial or are interested in learning Python,
go check it out. It's a great hands-on way for learning all about programming
in Python.

* _Learning Python The Hard Way_, online version and videos: 
http://learnpythonthehardway.org/book/

* Full book: http://learnpythonthehardway.org

## Starting from the Terminal

To try the example application, type the following in the terminal:

```
cd ex50
python bin/app.py
```

Alternatively, open the file in ex50/bin and click the green Run
button!

## Configuration

You can configure your Python version and `PYTHONPATH` used in
Cloud9 > Preferences > Project Settings > Language Support.

## Support & Documentation

Visit http://docs.c9.io for support, or to learn more about using Cloud9 IDE.
To watch some training videos, visit http://www.youtube.com/user/c9ide.
=======
# Installation
Install and run the main server by first instaling dependencies, starting the database then starting the server.

### Installing Dependencies
Befor you can start the main server, you will need to install the following dependencies on ubuntu 14.06<br/>
```sudo apt-get install python-pip python-dev libmysqlclient-dev```<br/>
```sudo apt-get install virtualenv```<br/>

### Setting up Database
1. Install mysql-server (if not already installed)<br/>
```sudo apt-get update```<br/>
```sudo apt-get install mysql-server```<br/>
optional if password prompt does not appear
```mysql_secure_installation```<br/>

2. Use flask-migrate.py after starting virtual environment to setup tables in db

### Setting up The Server
1. Create virtual environement `msvenv` <br/>
```virtualenv msvenv```<br/>
2. Activate newly created environment<br/>
```source venv/bin/activate```<br/>
3. Install requirements<br/>
```pip install -r requirements.txt```<br/>
4. Run application<br/>
```python run.py```
>>>>>>> 9a4cfbd2fcc85dd5fa32e0ccb2e61ab5a6be9018
