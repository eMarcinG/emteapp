#
# emteapp
#

# Multi-Tenant Management System

A multi-tenant management system built with Django and Django REST Framework (DRF). 
This application supports tenant-based data isolation, middleware for tenant identification, 
and API endpoints for managing tenants, organizations, departments, and customers.

## Features

- Tenant-based data isolation using custom middleware
- RESTful API endpoints for managing tenants, organizations, departments, and customers
- Docker support for easy deployment and development

## Requirements

- Docker
- Docker Compose

## Installation

### Step 1: Clone the repository

git clone https://github.com/eMarcinG/emteapp.git

### Step 2: Copy a .env file included into email.

Copy attached .env file into the base project ( added to email )

### Step 3:  Build and run Docker containers

Build and run the Docker containers using Docker Compose:

docker-compose up --build

please note: 
* initial data fixtures will be load automatically by docker from /management/fixtures/fixtures.json 
* superuser account will be created automatically based on .env data

#### Usage

# Accessing the Admin Panel

Accessing the Admin Panel
You can access the Django admin panel by navigating to http://localhost:8000/admin 
and logging in with the superuser credentials.

# Accessing the API

The API endpoints are available at http://localhost:8000/api/.

please note:
It is highly recommended to instal REST Client extension (for Visual Studio Code) 
and simply use the file "new.http" with all available endpoints.

# Users groups and permissions

There are three ways to create users in this project:

Using the Superuser Account via the Admin Panel:

1. You can create users using the Django admin panel with your superuser account. 
Simply log in to the admin panel at http://localhost:8000/admin/, 
navigate to the "Users" section, and add new users as needed.

2. Importing Fixtures from the fixtures_users.json File:

Another method is to load user data from the fixtures_users.json file. 
To do this, make sure the file is placed in the management/fixtures/ directory and run the following command:

python manage.py loaddata management/fixtures/fixtures_users.json

Users:

    admin: A superuser who can perform any operation.

    adminuser: An admin who has permission to read all resources without tenant middleware checks.

    readonlyuser: A standard user with double tenant verification enforced by middleware.

Note:

    Please change the users' passwords.

    Assign a tenant to readonlyuser user.

    Add the tenant domain in ALLOWED_HOSTS in the .env file.


3. Running the create_test_users.py Script:

You can also create test users by running the create_test_users.py script. Ensure that the script is placed in the root directory of the project and execute the following command:

python create_test_users.py


# Development
Running Tests
To run tests, use the following command:

docker-compose exec web python manage.py test

# Contributing
Contributions are welcome! 
Please create a pull request or open an issue for any improvements or bugs.

# License
This project is licensed under the MIT License. 