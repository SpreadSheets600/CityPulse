@echo off
echo Setting up database...
cd backend
uv run python -c "from app import create_app, create_db; app = create_app(); ctx = app.app_context(); ctx.push(); create_db()"
if %errorlevel% neq 0 (
    echo Database setup failed!
    cd ..
    exit /b %errorlevel%
)
echo Database ready.

echo Starting backend and frontend...
cd ..
start "CityPulse Backend" cmd /c "cd backend && uv run python app.py"
start "CityPulse Frontend" cmd /c "cd frontend && npm run dev"

echo Done. Both backend and frontend have been launched in separate windows.
