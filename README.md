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

git clone https://github.com/yourusername/multi-tenant-management.git
cd multi-tenant-management

### Step 2: Copy a .env file included into email.

Copy atached .env file into the base project

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

# Development
Running Tests
To run tests, use the following command:

docker-compose exec web python manage.py test

# Contributing
Contributions are welcome! 
Please create a pull request or open an issue for any improvements or bugs.

# License
This project is licensed under the MIT License. 