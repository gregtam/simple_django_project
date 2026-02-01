Render deployment notes
-----------------------

Environment variables to set on Render:

- `SECRET_KEY`: a strong, unique Django secret key
- `DJANGO_DEBUG`: set to `False`
- `ALLOWED_HOSTS`: comma-separated hostnames (e.g. `myapp.onrender.com`)
- (optional) `DATABASE_URL`: if you use Postgres; otherwise default is sqlite

Deployment steps on Render (web service):

1. Ensure `requirements.txt` and `Procfile` are in the repo.
2. Set the environment variables in the Render dashboard.
3. Deploy the service; Render will run `gunicorn simple_django_project.wsgi`.
4. After deploy, run migrations and collectstatic (via Render dashboard shell):

```
python manage.py migrate
python manage.py collectstatic --noinput
```

Notes:
- We use WhiteNoise for static file serving. `STATIC_ROOT` is `staticfiles`.
- For production database use, configure `DATABASE_URL` and install Postgres add-on.
