# fuerte.

A curated Fuerteventura service directory built with Django.

## Run locally

```bash
python3 -m pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver
```

## Deploy on Railway

1. Push this project to GitHub and create a Railway service from the repository.
2. Add PostgreSQL to the Railway project.
3. Set `DATABASE_URL=${{Postgres.DATABASE_URL}}` on the web service.
4. Set `DEBUG=False` and a strong, unique `SECRET_KEY`.
5. Generate a public domain in the service Networking settings.
6. Deploy. Railway will collect static files, migrate the database, start Gunicorn, and check `/health/`.

Create the production administrator after deployment with `railway run python manage.py createsuperuser`.
