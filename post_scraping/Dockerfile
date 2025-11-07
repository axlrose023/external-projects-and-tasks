FROM python:3.10-slim

WORKDIR /usr/src/app/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    bash \
    curl \
    libwebp-dev \
    g++ \
    gcc \
    git \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxcomposite1 \
    libxrandr2 \
    libxdamage1 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .

RUN pip install --upgrade pip wheel && \
    pip install -r requirements.txt --no-cache-dir

RUN python -m playwright install --with-deps

COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
