# CityPulse Deployment Guide

## Prerequisites

- Python 3.13+
- Node.js 18+
- PostgreSQL 14+ (or SQLite for dev)
- `uv` (Python package manager)
- `npm` (Node package manager)
- Docker & Docker Compose (for containerized deployment)

---

## Local Development

### 1. Clone & Setup

```bash
git clone <repo-url>
cd CityPulse
```

### 2. Backend Setup

```bash
cd backend
uv sync
cp .env.example .env
# Edit .env with your database credentials
uv run flask db init
uv run flask db migrate -m "Initial migration"
uv run flask db upgrade
uv run flask run --debug --port 5000
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### 4. Run Both (Recommended)

```bash
chmod +x devserver.sh
./devserver.sh
```

| Service | URL |
|---------|-----|
| Backend | `http://localhost:5000` |
| Frontend | `http://localhost:5173` (proxies `/api` to backend) |

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | Yes | Hardcoded fallback | Flask secret key |
| `SQLALCHEMY_DATABASE_URI` | Yes | `sqlite:///citypulse.db` | Database connection string |
| `JWT_SECRET_KEY` | Yes | Hardcoded fallback | JWT signing key |
| `S3_ENDPOINT` | No | Synology C2 endpoint | S3 endpoint URL |
| `S3_ACCESS_KEY` | No | Hardcoded | S3 access key |
| `S3_SECRET_KEY` | No | Hardcoded | S3 secret key |
| `S3_BUCKET` | No | `citypulse` | S3 bucket name |
| `S3_REGION` | No | `us-003` | S3 region |
| `CORS_ORIGINS` | No | `*` | Comma-separated allowed origins |
| `MAIL_SERVER` | No | `localhost` | SMTP server |
| `MAIL_PORT` | No | `25` | SMTP port |
| `GOOGLE_CLIENT_ID` | No | - | Google OAuth client ID |
| `GOOGLE_CLIENT_SECRET` | No | - | Google OAuth secret |
| `GITHUB_CLIENT_ID` | No | - | GitHub OAuth client ID |
| `GITHUB_CLIENT_SECRET` | No | - | GitHub OAuth secret |

**Example `.env`:**
```env
SECRET_KEY=your-super-secret-key-here
SQLALCHEMY_DATABASE_URI=postgresql://postgres:password@localhost:5432/citypulse
JWT_SECRET_KEY=your-jwt-secret-key-here
CORS_ORIGINS=http://localhost:5173,https://your-domain.com
```

---

## Testing

### Backend Tests

```bash
cd backend
PYTHONPATH=. uv run pytest tests/ -v
PYTHONPATH=. uv run pytest tests/test_models.py -v
PYTHONPATH=. uv run pytest tests/ -v --tb=short
```

| Test file | Description |
|-----------|-------------|
| `test_models.py` | User and Issue model tests |
| `test_auth.py` | Authentication endpoint tests |
| `test_issues.py` | Issue CRUD endpoint tests |
| `test_integration.py` | Full lifecycle integration tests |
| `test_intelligence.py` | AI classification, duplicate detection, priority scoring |

### Frontend Tests

```bash
cd frontend
npx vitest run
npx vitest  # watch mode
```

---

## Docker Deployment

### CI/CD Pipeline

```mermaid
flowchart LR
    A[Push to main/develop] --> B[GitHub Actions]
    B --> C[Backend Tests<br/>Python 3.13 + pytest]
    B --> D[Frontend Tests<br/>Node 20 + vitest]
    C --> E[Docker Build]
    D --> E
    E --> F[Push Images]
    F --> G[Deploy]
```

### Using Docker Compose (Recommended)

```bash
docker compose up -d
docker compose logs -f
docker compose down
```

| Service | Port | Description |
|---------|------|-------------|
| PostgreSQL | 5432 | Database |
| Backend | 5000 | Flask + gunicorn |
| Frontend | 80 | Nginx |

### Building Individual Images

```bash
cd backend && docker build -t citypulse-backend .
cd frontend && docker build -t citypulse-frontend .
```

### Docker Compose Services

```yaml
services:
  db:       # PostgreSQL 16 Alpine
  backend:  # Python 3.13 + gunicorn
  frontend: # Node build + nginx
```

---

## Production Deployment

### 1. Database

```bash
psql -U postgres -c "CREATE DATABASE citypulse;"
cd backend && uv run flask db upgrade
```

### 2. Backend

```bash
export SECRET_KEY=$(openssl rand -hex 32)
export JWT_SECRET_KEY=$(openssl rand -hex 32)
export SQLALCHEMY_DATABASE_URI=postgresql://user:password@host:5432/citypulse
uv sync --no-dev
uv run gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

### 3. Frontend

```bash
cd frontend && npm run build
# Serve frontend/dist/ with nginx/apache
```

### 4. Nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /var/www/citypulse/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    client_max_body_size 20M;
}
```

---

## Security Checklist for Production

- [x] Move S3 credentials to environment variables
- [x] Restrict CORS origins to your domain
- [x] Use strong, unique `SECRET_KEY` and `JWT_SECRET_KEY`
- [ ] Enable HTTPS (SSL/TLS)
- [ ] Set `FLASK_ENV=production`
- [x] Configure proper database connection pooling
- [ ] Set up database backups
- [x] Add rate limiting to API endpoints
- [ ] Review and restrict file upload types
- [ ] Set up monitoring and logging

---

## Troubleshooting

| Issue | Diagnosis |
|-------|-----------|
| **Database connection refused** | `sudo systemctl status postgresql` · `psql -U postgres -c "\l"` |
| **S3 upload fails** | `aws s3 ls s3://citypulse --endpoint-url https://us-003.s3.synologyc2.net` |
| **Frontend can't reach API** | `curl http://localhost:5000/ping` · Check `vite.config.js` proxy |
| **JWT token expired** | `POST /api/auth/refresh` with `Authorization: Bearer <refresh_token>` |
| **Docker build fails** | `docker info` · `docker compose build --no-cache` |
