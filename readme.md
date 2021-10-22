# SocialFeed - social media app

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Features](#features)
* [To do](#to-do)
* [Setup](#setup)
* [Inspiration](#inspiration)

## General info

Simple social media app created with Django for educational purpose. My main focus was to conslidate knowledge acquired during doing tutorials, especially to create CRUD with accounts, write tests. App is created only by me.

![Alt text](static/images/screens/screen1.png "Login Page")
![Alt text](static/images/screens/screen2.png "Dashboard")
![Alt text](static/images/screens/screen3.png "Profile")
![Alt text](static/images/screens/screen4.png "Viewing users and dropdown list")


## Technologies

 - Python 3.8
 - Django 3.1
 - PostgreSQL
 - Bootstrap 4
 - AWS RDS and S3
 - Heroku
 - Unittest
 
## Features

 - Registration
 - Changing / reseting password
 - Updating profile
 - CRUD posts and comments
 - Adding likes to posts
 - Sending, accepting and rejecting invitations
 - Deleting from friends
 - Searching users
 - Adding profile picture
 - Pagination
 
## To do

 - Notifications about friends' actions
 - Advance search
 - Chat
 - User's picture gallery
 - Posting pictures, films etc on wall

## Setup 

Clone repo `git clone https://github.com/MateuszM-M/SocialFeed`,

Go to repo directory `cd SocialFeed`,

Create virtual environment `python -m venv venv`,

Activate environment `venv\scripts\activate`,

Install required packages `pip install -r requirements.txt`,

Rename MMblog/settings/`.env-example` to `.env`,

Create local postgres database and type credentials in SocialFeed/settings/dev.py

Migrate database `python manage.py migrate`,

Create superuser `python manage.py createsuperuser`,

Make server up and running `python manage.py runserver`,

Browse http://127.0.0.1:8000/

Or

Online demo: https://hello-social-feed.herokuapp.com/

## Inspiration

 Some parts of code are inspired from:
 - Book: Django 2 by Example by Antonio Mele - mainly account part
 - Tutorial: https://www.youtube.com/watch?v=ozr6NEomLQw&list=PLgjw1dR712joFJvX_WKIuglbR1SNCeno1&ab_channel=Pyplane - adding friends, adding likes
