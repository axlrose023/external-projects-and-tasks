
# Spy Cat Agency Management Application

This is a Django-based RESTful API application for managing spy cats, their missions, and targets for the Spy Cat Agency (SCA). The application allows you to perform CRUD operations on spy cats and missions, assign cats to missions, and manage mission targets.

## Table of Contents

- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
  - [Spy Cats](#spy-cats)
  - [Missions](#missions)
  - [Targets](#targets)
- [Postman Collection](#postman-collection)
- [Notes](#notes)

## Project Overview

The Spy Cat Agency Management Application provides the following features:

- **Spy Cats**: Create, retrieve, update, and delete spy cats.
- **Missions**: Create missions with targets, assign cats to missions, and manage mission completion.
- **Targets**: Update target notes and mark targets as complete.

## Prerequisites

Make sure you have the following installed on your system:

- Python 3.6 or higher
- pip (Python package manager)
- Git (optional, for cloning the repository)

## Installation

Follow these steps to set up the project locally:

1. **Clone the Repository** (if applicable):

   ```bash
   git clone https://github.com/axlrose023/test-task_DevTodays.git
   cd developsToday
   ```

2. **Create a Virtual Environment** (optional but recommended):

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a Superuser** (optional, for accessing the Django admin interface):

   ```bash
   python manage.py createsuperuser
   ```

## Running the Application

Start the development server with the following command:

```bash
python manage.py runserver
```

The application will be accessible at `http://localhost:8000/`.

## API Endpoints

Below is a list of available API endpoints with their descriptions:

### Spy Cats

- **List Spy Cats**

  ```
  GET /spycats/
  ```

- **Create a Spy Cat**

  ```
  POST /spycats/
  ```

  **Request Body**:

  ```json
  {
    "name": "Whiskers",
    "years_of_experience": 5,
    "breed": "Siamese",
    "salary": 50000.00
  }
  ```

- **Retrieve a Spy Cat**

  ```
  GET /spycats/{id}/
  ```

- **Update a Spy Cat**

  ```
  PATCH /spycats/{id}/
  ```

  **Request Body** (example):

  ```json
  {
    "salary": 55000.00
  }
  ```

- **Delete a Spy Cat**

  ```
  DELETE /spycats/{id}/
  ```

### Missions

- **List Missions**

  ```
  GET /missions/
  ```

- **Create a Mission**

  ```
  POST /missions/
  ```

  **Request Body**:

  ```json
  {
    "cat": null,
    "targets": [
      {
        "name": "Target Alpha",
        "country": "Country X",
        "notes": ""
      },
      {
        "name": "Target Beta",
        "country": "Country Y",
        "notes": ""
      }
    ]
  }
  ```

- **Retrieve a Mission**

  ```
  GET /missions/{id}/
  ```

- **Update a Mission**

  ```
  PATCH /missions/{id}/
  ```

  **Note**: Updating targets through mission update is not supported.

- **Delete a Mission**

  ```
  DELETE /missions/{id}/
  ```

  **Note**: Cannot delete a mission if it's assigned to a cat.

- **Assign a Cat to a Mission**

  ```
  POST /missions/{id}/assign_cat/
  ```

  **Request Body**:

  ```json
  {
    "cat_id": 1
  }
  ```

- **Mark a Mission as Complete**

  ```
  POST /missions/{id}/complete/
  ```

  **Note**: All targets must be completed before completing the mission.

### Targets

- **List Targets**

  ```
  GET /targets/
  ```

- **Retrieve a Target**

  ```
  GET /targets/{id}/
  ```

- **Update a Target**

  ```
  PATCH /targets/{id}/
  ```

  **Request Body** (example):

  ```json
  {
    "notes": "Updated notes on the target."
  }
  ```

- **Mark a Target as Complete**

  ```
  POST /targets/{id}/complete/
  ```

## Postman Collection

To simplify API testing, you can import the following Postman collection:

1. **Copy the JSON below and save it as `SCA_Postman_Collection.json`**:

   ```json
   {
     "info": {
       "name": "Spy Cat Agency API",
       "_postman_id": "your-postman-id",
       "description": "Postman collection for Spy Cat Agency API",
       "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
     },
     "item": [
       {
         "name": "List Spy Cats",
         "request": {
           "method": "GET",
           "header": [],
           "url": {
             "raw": "http://localhost:8000/spycats/",
             "protocol": "http",
             "host": ["localhost"],
             "port": "8000",
             "path": ["spycats", ""]
           }
         },
         "response": []
       },
       {
         "name": "Create Spy Cat",
         "request": {
           "method": "POST",
           "header": [
             {
               "key": "Content-Type",
               "value": "application/json"
             }
           ],
           "body": {
             "mode": "raw",
             "raw": "{\n  "name": "Whiskers",\n  "years_of_experience": 5,\n  "breed": "Siamese",\n  "salary": 50000.00\n}"
           },
           "url": {
             "raw": "http://localhost:8000/spycats/",
             "protocol": "http",
             "host": ["localhost"],
             "port": "8000",
             "path": ["spycats", ""]
           }
         },
         "response": []
       }
     ]
   }
   ```

2. **Import the Collection into Postman**:

   - Open Postman.
   - Click on `Import` in the top-left corner.
   - Select `File` and choose the `SCA_Postman_Collection.json` file you saved.
   - The collection will be imported and available for use.

**Note**: Adjust the host and port in the collection if your application is running on a different address.

## Notes

- **Breed Validation**: The application validates cat breeds using [TheCatAPI](https://api.thecatapi.com/v1/breeds). Ensure you have an active internet connection when creating or updating spy cats.

- **Error Handling**: The API returns appropriate HTTP status codes and error messages for invalid requests. For example, attempting to delete a mission assigned to a cat will return a `400 Bad Request` with an error message.

- **Data Formats**: All request and response bodies are in JSON format.

- **Authentication**: This application does not include authentication mechanisms. For production use, consider adding authentication and permissions.

- **Testing**: Automated tests are included in the `tests` file. Run them with:

  ```bash
  python manage.py test
  ```

- **Admin Interface**: Access the Django admin interface at `http://localhost:8000/admin/` using the superuser account you created earlier.

---
