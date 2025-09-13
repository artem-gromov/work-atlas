# WorkAtlas

Backend service for locating remote teammates on a map. This repository
contains a Django project configured for multi‑tenancy using
[`django-tenants`](https://django-tenants.readthedocs.io/). Each tenant has
its own PostgreSQL schema and can manage employee profiles with geospatial
data powered by PostGIS.

## Development

```bash
make up        # start containers
make migrate   # run migrations for public and tenant apps
```

Create the first tenant:

```bash
python manage.py create_tenant --name "Acme" --domain acme.app.local --schema acme
```

OpenAPI docs are available at `http://<tenant>.app.local:8000/api/docs/` and
the raw schema at `/api/schema/`.

## File storage

In production the project can store uploaded files on S3. Configure the
following environment variables (see `.env.example`):

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME
AWS_S3_REGION_NAME
```

When developing locally files are stored under `media/` using the default
Django file storage backend.

