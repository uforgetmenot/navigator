#!/bin/bash
set -euo pipefail

DB_URL="${DATABASE_URL:-sqlite:///./navigator.db}"
DB_PATH=""

if [[ "$DB_URL" == sqlite:* ]]; then
  DB_PATH="${DB_URL#sqlite:///}"
  if [[ ! "$DB_PATH" = /* ]]; then
    DB_PATH="/app/${DB_PATH#./}"
  fi
  mkdir -p "$(dirname "$DB_PATH")"
  if [[ ! -f "$DB_PATH" ]]; then
    echo "[entrypoint] Initializing database at $DB_PATH"
    python -m app.services.seed
  fi
fi

exec "$@"
