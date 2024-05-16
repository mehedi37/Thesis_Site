#!/bin/bash

# Get the project name
echo "Enter your Django project name:"
read project_name

# Create a virtual environment
python -m venv env

# Activate the virtual environment
source env/Scripts/activate

# Install Django
pip install django

# Start a new Django project
django-admin startproject $project_name .

code .

echo "Django project setup completed."

# env/Scripts/Activate.ps1


# More django commands
# python manage.py runserver 8000
# python manage.py makemigrations
# python manage.py migrate
# python manage.py createsuperuser
# python manage.py flush