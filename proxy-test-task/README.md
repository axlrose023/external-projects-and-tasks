# Test Task Project

This Django project was generated with Django 4.2.7 and includes settings for PostgreSQL as the database. Docker Compose is used for containerized development.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

### 1. Clone the Repository

git clone https://github.com/axlrose023/proxy-test-task

cd proxy-test-task

### 2. Set Up Environment Variables
DJANGO_SECRET_KEY=your_secret_key

DEBUG=True

ALLOWED_HOSTS=localhost,127.0.0.1

### 3. Run with Docker Compose
docker-compose up --build

### Additional Notes
- Make sure to customize the Django secret key and other settings in the .env file for security.
- Update the ALLOWED_HOSTS setting in production to match your domain.
- For production, consider using a more secure method for managing secrets.