# fuerte.

A visual, self-managed showcase connecting Fuerteventura's portals, projects and people.

## Run locally

```bash
python3 -m pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver
```

Open `/admin/` to manage homepage settings, showcase cards, sponsor banners and team profiles. Every showcase record supports ordering and an active/inactive switch. Images can be uploaded directly or supplied as external URLs.

For production uploads, attach a Railway Volume to the web service. The application automatically stores uploads under `media/` inside Railway's `RAILWAY_VOLUME_MOUNT_PATH`; without a volume, Railway's application filesystem is ephemeral.

## Deploy on Railway

1. Push this project to GitHub and create a Railway service from the repository.
2. Add PostgreSQL to the Railway project.
3. In the **web service** variables, add a Railway reference variable named `DATABASE_URL` with the value `${{Postgres.DATABASE_URL}}` (replace `Postgres` if your database service has a different name). Do not paste a temporary public URL.
4. Attach a Railway Volume to the **web service** with mount path `/data`. Railway supplies `RAILWAY_VOLUME_MOUNT_PATH` automatically; do not create that variable manually. Uploaded collaboration, business, team and homepage images will be stored under `/data/media`.
5. Set `DEBUG=False` and a strong, unique `SECRET_KEY`.
6. Generate a public domain in the service Networking settings.
7. Deploy. Railway will collect static files, migrate the database, start Gunicorn, and check `/health/`.

Create the production administrator once after PostgreSQL is connected with `railway run python manage.py createsuperuser`. The account and all admin-managed content will then survive redeployments because they live in PostgreSQL.

Production deliberately refuses to start without `DATABASE_URL`. This prevents an accidental fallback to Railway's ephemeral filesystem, which would otherwise create a fresh SQLite database and lose users on every redeployment.

## Persistent production data

- PostgreSQL stores superusers, collaborations, businesses, team members, site settings, articles and every other model record.
- The attached `/data` volume stores images uploaded through Django admin.
- Repository assets, including the generated default business covers, are deployed from Git and do not require the volume.

Enable Railway backups for both the PostgreSQL service and the web-service volume. A redeployment does not delete either one, but backups protect against accidental edits or manual deletion.
