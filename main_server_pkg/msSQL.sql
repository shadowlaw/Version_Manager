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

CREATE TABLE nodes(
id int(10) auto_increment not null,
name varchar(255) not null,
password varchar(255) not null,
api_key varchar(255),
primary key (id)
);

INSERT INTO users(first_name, last_name, username, password) VALUES ('Javed', 'Wright', 'admin', 'pbkdf2:sha1:1000$nMULFvbx$f57dfe0db262317468320afb37fec65716d1b64b');