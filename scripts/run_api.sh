#!/usr/bin/env bash
# Usage: source venv, then run this script
# Example:
#   source .venv/bin/activate
#   ./scripts/run_api.sh

UVICORN_HOST=${UVICORN_HOST:-127.0.0.1}
UVICORN_PORT=${UVICORN_PORT:-8000}
UVICORN_WORKERS=${UVICORN_WORKERS:-1}

exec uvicorn backend.app.main:app --host "$UVICORN_HOST" --port "$UVICORN_PORT" --workers "$UVICORN_WORKERS" --reload
