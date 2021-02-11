# Alias_test
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
This project is custom checks and constraints that will ensure validity of alias records. 
The "start" and "end" fields specify the time range in which the Alias is active.
Aliases may overlap (for the same target​ ) as long as alias​ value is different.
Aliases may have the same alias​ value (for the same target​ ) as long as they do not overlap.
It should not be allowed to have aliases
"useful-object" and "useful-object" pointing to the same target​ from 2020-01-01​ to 2020-02-01
and from 2020-01-31​ to 2020-02-05​ (note overlap at 01-31​ ).
	
## Technologies
Project is created with:
* Django==3.0
* psycopg2-binary==2.8.6


	
## Setup
To run this project, install it locally using:

```
$ git clone git@github.com:OleksandrPichkurov/Alias_test.git
$ pip3 install -r requirements.txt
```
In the root folder of the project, create local_settings.py and add settings:
```
$ touch local_settings.py
$ sudo nano local_settings.py


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dbname',
        'USER': 'dbuser',
        'PASSWORD': '123456789',
        'HOST': '',
    }
}

```
Create database and user:
```
$ sudo su postgres
$ psql
$ CREATE DATABASE dbname;
$ CREATE USER dbuser WITH password '123456789';
$ GRANT ALL ON DATABASE dbname TO dbuser;
$ ALTER USER dbuser CREATEDB;
```
Run migration
```
$ python3 manage.py migrate
```
Run test
```
$ python3 manage.py test alias
```