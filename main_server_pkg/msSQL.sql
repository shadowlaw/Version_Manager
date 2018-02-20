DROP DATABASE IF EXISTS vm_main_server;
CREATE DATABASE vm_main_server;
USE vm_main_server

CREATE TABLE users(
id int(10) auto_increment,
first_name varchar(80) not null,
last_name varchar(80) not null,
username varchar(80) not null,
password varchar(225) not null,
primary key (id)
);