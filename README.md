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

2. Create the database<br/>

3. Use flask-migrate.py after starting virtual environment to setup tables in db

### Setting up Workbench, backend server and client
From the server source code root directory:
1. Create virtual environement `venv` <br/>
```virtualenv msvenv```<br/>
2. Activate newly created environment<br/>
```source venv/bin/activate```<br/>
3. Install requirements<br/>
```pip install -r requirements.txt```<br/>
4. Run application<br/>
```python run.py```
