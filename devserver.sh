#!/bin/bash

set -e

cleanup() {
  echo ""
  echo "Shutting down..."
  kill 0 2>/dev/null
  exit
}
trap cleanup SIGINT SIGTERM

# Setup database
echo "Setting up database..."
(
  cd backend
  uv run python -c "
from app import create_app, create_db
app = create_app()
with app.app_context():
    create_db()
" 2>&1 | grep -E "(INFO|ERROR|Created|Admin|Email|Password)"
)
echo "Database ready."

# Start backend
(
  cd backend
  echo "Starting Flask Backend on http://localhost:5000 ..."
  uv run python app.py
) &

# Start frontend
(
  cd frontend
  echo "Starting Vue Frontend on http://localhost:5173 ..."
  npm run dev
) &

wait
