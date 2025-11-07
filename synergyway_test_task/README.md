
Build and start the project using Docker:
  docker-compose up --build

The application will be available at:
  http://localhost:8000


A FastAPI endpoint is available to fetch user data.
  GET /users/

Celery tasks for fetching user data run automatically. You can adjust the execution intervals in the Celery configuration.
