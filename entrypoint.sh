#!/usr/bin/sh
set -e

: "${GUNICORN_WORKERS:=4}"

echo "Apply migrations"
alembic upgrade head

echo "Starting application..."
exec gunicorn app.main:app \
  --worker-class uvicorn.workers.UvicornWorker \
  --workers "$GUNICORN_WORKERS" \
  --bind 0.0.0.0:8000 \
  --timeout "$GUNICORN_TIMEOUT" \
  --keep-alive "$GUNICORN_KEEPALIVE" \
  --access-logfile - \
  --error-logfile - \
  --log-level info
