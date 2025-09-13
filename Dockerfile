FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml /app/
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-root

COPY . /app

COPY docker/entrypoint.sh /start
RUN chmod +x /start

