<h1 align="center"> Tidbits </h1> <br>
<p align="center">
  <a href="https://gitpoint.co/">
    <img alt="GitPoint" title="GitPoint" src="https://i.imgur.com/NhkTg5U.png" width="450">
  </a>
</p>

<p align="center">
  by Marcello Guglielmi
</p>

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Table of Contents

- [Introduction](#introduction)
- [Key Features](#key-features)
- [User Section](#user-section)
- [Moderation](#admin-section)
- [Miscellaneous](#misc)
- [Project Download](#installation)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Introduction

![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)
![Python](https://img.shields.io/badge/python-3.13-yellow.svg?style=flat-square)
![Django](https://img.shields.io/badge/django-5.0-green.svg?style=flat-square)
![Last Commit](https://img.shields.io/github/last-commit/cello-guglielmi/tidbits?style=flat-square)
![Quotes](https://img.shields.io/badge/quotes-inspirational-orange?style=flat-square)

Tidbits is a  quote curation and display platform. Built with a Django framework  and coded in Python 3.13. Includes user interactivity, content submission and administrative moderation. Supports both desktop and mobile layouts.

<p align="center">
  <img src = "https://i.imgur.com/JTFiMDt.gif">
</p>

## Key Features

A few of the things you can do with GitPoint:

* Daily Quote landing page - Pleasing asthetics and rotating assortment.
* Quote list repository - With filtering & sorting mechanisms.
* Author list repository - With filtering, sorting, and invidual profiles
* User account Creation/Login
* Quote "Like" counter and "Bookmark" option.
* User submissions - Complete with moderation approval workflows.
* Administrative custom panel - Refactored from Django's pre-built admin.


## Repository Browsing

Both quotes and artists repositories boast intricate and intuitive filtering & sorting options, with a realtime text search bar, selectable mood tags, and alphabetical / by author / by mood / by like count sorting buttons.

<p align="center">
  <img align="top" src = "https://i.imgur.com/XQ3bk0X.png" width=500>
  <span>
  <img src = "https://i.imgur.com/6M0OUSN.gif" width=300>
</p>


## User Profile

Users are free to browse anonymously,  but are welcome to make an account to be able to provide their own quote submissions and bookmark their favorite quotes!
<p align="center">
  <img src = "https://i.imgur.com/79dbO9u.gif" width=900>
</p>

<p align="center">
  <img src = "https://i.imgur.com/s3L1Zql.gif" width=600>
</p>

<p align="center">
  <img src = "https://i.imgur.com/vvpS729.gif" width=700>
</p>

## Moderation

The app generates "Submission" objects for user submitted content (both quote or author). These can be approved by moderation via a customized interface. Once properly filled & approved, Submissions get retired and proper Quote or Author objects get automatically inserted into the database for public display! Additionally, an email notification is sent to the submitting user both on approval or rejection.

<p align="center">
  <img src = "https://i.imgur.com/3d1F0Pp.png" width=500>
</p>

<p align="center">
  <img src = "https://i.imgur.com/sD6WpXe.gifg" width=900>
</p>

## Miscellaneous

<p align="center">Author Profile</p>
<p align="center">
  <img src = "https://i.imgur.com/ULdRPbd.gif" width=700>
</p>

<p align="center">Help Page</p>
<p align="center">
  <img src = "https://i.imgur.com/Ssm98fE.png" width=1200>
</p>

## Project Download

<a href="https://gist.github.com/cello-guglielmi/0086aa6c26a8978f3809bd39ecbb93ab">Click here</a> for the Github Gist version of these instructions!

### How to run this Dockerized Django app

1. Clone the Django project and put these Docker files in the root folder.

2. Open a terminal in that folder.

3. Build and run the container: docker compose up --build

4. Visit http://localhost:8000 in your browser.

**docker-compose.yml**
```
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
```

**dockerfile**
```
# Use official Python image
FROM python:3.13.2-slim

# Set environment vars
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy Django project files into the container
COPY . .

# Run Django dev server (adjust the host/port if needed)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```
