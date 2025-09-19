#!/bin/bash

trap "kill 0" EXIT

(
  cd backend || exit
  echo "🚀 Starting Flask Backend ..."

  uv run app.py
) &


(
  cd frontend || exit
  echo "💻 Starting Vue Frontend ..."

  npm run dev
) &

wait
