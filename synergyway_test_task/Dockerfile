FROM python:3.10-slim

WORKDIR /usr/src/app/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y bash curl libwebp-dev g++ gcc git

COPY ./requirements.txt .

RUN pip install --upgrade pip wheel && \
    pip install -r requirements.txt --no-cache-dir

COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
