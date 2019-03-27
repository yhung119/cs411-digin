Added very basic polling system with vote counting based on the tutorial at https://docs.djangoproject.com/en/1.10/intro/tutorial01/

# CS411 Final Project - Digin

## Set up database
1. Create table: CREATE DATABASE db_name CHARACTER SET UTF8;
2. run setup.sh
    ```sh
    chmod +x ./setup.sh
    ./setup.sh
    ```
3. check if tables are created accordingly and application works
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
