web: gunicorn "app:create_app()"
worker: celery -A app.celery worker --loglevel=info  # Adjust according to your app structure
