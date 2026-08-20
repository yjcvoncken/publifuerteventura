# fuerte.

A visual, self-managed showcase connecting Fuerteventura's portals, projects and people.

## Run locally

```bash
python3 -m pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver
```

Open `/admin/` to manage homepage settings, showcase cards, sponsor banners and team profiles. Every showcase record supports ordering and an active/inactive switch. Images can be uploaded directly or supplied as external URLs.

For production uploads, attach persistent storage at the configured `media/` directory (or replace Django's default storage with an object-storage backend). Uploaded files are served by Django in this first phase; move them to object storage/CDN as traffic grows. Railway's application filesystem is otherwise ephemeral.

## Deploy on Railway

1. Push this project to GitHub and create a Railway service from the repository.
2. Add PostgreSQL to the Railway project.
3. Set `DATABASE_URL=${{Postgres.DATABASE_URL}}` on the web service.
4. Set `DEBUG=False` and a strong, unique `SECRET_KEY`.
5. Generate a public domain in the service Networking settings.
6. Deploy. Railway will collect static files, migrate the database, start Gunicorn, and check `/health/`.

Create the production administrator after deployment with `railway run python manage.py createsuperuser`.
