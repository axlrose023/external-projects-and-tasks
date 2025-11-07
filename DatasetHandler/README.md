# FancyData API & SDK

A minimal **FastAPI** service (Postgres backend) with an **async Python SDK**.

---

## ⛳️ Overview

- **API**: FastAPI + Uvicorn  
- **DB**: PostgreSQL 15 (via Docker)  
- **SDK**: Async (uses `httpx.AsyncClient`)  
- **Docs**: Swagger UI at **`http://localhost:8080/docs`** (see port mapping below)

---

## ✅ Prerequisites

- Docker & Docker Compose
- (Optional) `.env` file with Postgres vars:
  ```env
  DOCKER_POSTGRES_PASSWORD=password
  DOCKER_POSTGRES_USER=user
  DOCKER_POSTGRES_DB=db
  DOCKER_POSTGRES_PORT=5432
  DOCKER_POSTGRES_HOST=postgres
  ```

---

## 🚀 Quick Start

### 1) Build & start the stack

```bash
docker-compose up --build
```

This brings up:

- `app` — FastAPI app (served by Uvicorn)
- `postgres` — PostgreSQL 15

### 2) Port mapping

The app listens on **`8000`** **inside** the container.

If you want Swagger at **`http://localhost:8080/docs`**, expose it as **`8080:8000`**:

```yaml
# docker-compose.yml
services:
  app:
    ports:
      - "8080:8000"    # host:container
```

If you keep the default mapping **`8000:8000`**, then use **`http://localhost:8000/docs`** instead.

### 3) API docs (Swagger/OpenAPI)

- Swagger UI: **http://localhost:8080/docs**  
- OpenAPI JSON: **http://localhost:8080/openapi.json**

> Adjust port to `8000` if you kept `8000:8000`.

---

## 🧪 Run tests (inside the container)

Open a shell in the `app` service and run `pytest`:

```bash
docker-compose exec app pytest
```

---

## 🧰 Try the SDK manually (inside the container)

Run the SDK manual script from the `app` container:

```bash
docker-compose exec app python manual_test.py
```

The script will:

- create a dataset  
- list datasets  
- retrieve by id/name  
- add items (single & batch)  
- iterate all items & filtered items  
- show the expected error for a non-existent dataset

> **Note:** `manual_test.py` uses `api_url="http://localhost:8000/api"` by default.  
> If you mapped the app to port **8080**, update it to `http://localhost:8080/api`.

---

## 🧷 Useful Commands

```bash
# Build & start
docker-compose up --build

# Stop
docker-compose down

# Stop and remove volumes (Postgres data)
docker-compose down -v

# One-off shell inside the app container
docker-compose exec app bash

# Run tests
docker-compose exec app pytest

# Run SDK manual script
docker-compose exec app python manual_test.py
```

---

## 📂 Project Bits

- **Dockerfile** builds the app image and installs dependencies from `requirements.txt`.
- **docker-compose.yml** defines `app` and `postgres` services and maps ports/volumes.
- **Swagger** is served by FastAPI at `/docs` on the configured host port.
- **SDK** is async; the manual test script runs it via `asyncio.run(...)`.

---

## 💡 Troubleshooting

- **Swagger not opening on 8080**: ensure `app.ports` is set to `8080:8000`, or use `http://localhost:8000/docs` with `8000:8000`.
- **DB connection issues**: verify `.env` values match those in `docker-compose.yml`.
- **SDK cannot reach API**: confirm the base URL and port (`/api` prefix in `manual_test.py`).

---

Happy shipping! ✨
