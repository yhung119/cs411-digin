
# CS411 Final Project - Digin

## Current Schema
- user : UID, location, email, name, (later: pwd, authenticate)

  pk: UID
  
- poll : PID, owner, poll_name, eating_time, deadline_time, created_time, (later: participants)

  pk: PID

- choice : PID, UID, name, lat, long, vote

  pk: PID, UID, name

## Requirements
- python3
- mysql
- node.js / npm
- virtualenv / virtualenvwrapper

## Install 
```
# python libraries
pip install -r reqirements.txt

# set up mysql https://www.digitalocean.com/community/tutorials/how-to-use-mysql-or-mariadb-with-your-django-application-on-ubuntu-14-04
# (Mac) brew install mysql
# create data base
CREATE DATABASE test CHARACTER SET UTF8;

# create project usr and grant privilege
CREATE USER myprojectuser@localhost IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON myproject.* TO myprojectuser@localhost;
FLUSH PRIVILEGES;


# connect with mysql
touch ./digin/my.cnf

# fill in my.cnf
[client]
database = test
host = localhost
user = PROJECTUSER
password = PROJECTPASSWORD
default-character-set = utf8

# make migration
cd ./digin
python manage.py makemigrations
python manage.py migrate

# data in database should be shown on localhost
python manage.py runserver


# install frontend dependencies
npm install

```
