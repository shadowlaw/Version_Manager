# Installation
Install and run the main server by first instaling dependencies, starting the database then starting the server.

### Installing Dependencies
Befor you can start the main server, you will need to install the following dependencies on ubuntu 14.06<br/>
```sudo apt-get install python-pip python-dev libmysqlclient-dev```<br/>
```sudo apt-get install virtualenv```<br/>

### Setting up Database
1. Install mysql-server (if not already installed)
2. Use the msSQL.sql to create the database

### Setting up The Server
1. Create virtual environement `msvenv` <br/>
```virtualenv msvenv```<br/>
2. Activate newly created environment<br/>
```source msvenv/bin/activate```<br/>
3. Install requirements<br/>
```pip install -r requirements.txt```<br/>
4. Run application<br/>
```python run.py```
