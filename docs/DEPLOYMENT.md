# CityPulse Deployment Guide

## Prerequisites

- Python 3.13+
- Node.js 18+
- PostgreSQL 14+
- `uv` (Python package manager)
- `npm` (Node package manager)

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

# Install dependencies
uv sync

# Create .env file from template
cp .env.example .env

# Edit .env with your database credentials
# SQLALCHEMY_DATABASE_URI=postgresql://postgres:password@localhost:5432/citypulse

# Initialize database
uv run flask db init
uv run flask db migrate -m "Initial migration"
uv run flask db upgrade

# Start backend server
uv run flask run --debug --port 5000
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

### 4. Run Both (Recommended)

```bash
# From project root
chmod +x devserver.sh
./devserver.sh
```

This starts:
- Backend: `http://localhost:5000`
- Frontend: `http://localhost:5173` (proxies `/api` to backend)

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | Yes | Hardcoded fallback | Flask secret key |
| `SQLALCHEMY_DATABASE_URI` | Yes | `sqlite:///citypulse.db` | Database connection string |
| `JWT_SECRET_KEY` | Yes | Hardcoded fallback | JWT signing key |
| `S3_ENDPOINT` | No | `https://us-003.s3.synologyc2.net` | S3 endpoint URL |
| `S3_ACCESS_KEY` | No | Hardcoded | S3 access key ID |
| `S3_SECRET_KEY` | No | Hardcoded | S3 secret access key |
| `S3_BUCKET` | No | `citypulse` | S3 bucket name |
| `S3_REGION` | No | `us-003` | S3 region |

**Example `.env`:**
```env
SECRET_KEY=your-super-secret-key-here
SQLALCHEMY_DATABASE_URI=postgresql://postgres:password@localhost:5432/citypulse
JWT_SECRET_KEY=your-jwt-secret-key-here
```

### Frontend

The frontend uses Vite's proxy configuration (no env vars needed for dev).

For production, update `frontend/src/api/client.js`:
```javascript
const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000',
})
```

---

## Production Deployment

### 1. Database

```bash
# Create PostgreSQL database
psql -U postgres -c "CREATE DATABASE citypulse;"

# Run migrations
cd backend
uv run flask db upgrade
```

### 2. Backend

```bash
cd backend

# Set environment variables
export SECRET_KEY=$(openssl rand -hex 32)
export JWT_SECRET_KEY=$(openssl rand -hex 32)
export SQLALCHEMY_DATABASE_URI=postgresql://user:password@host:5432/citypulse

# Install production dependencies
uv sync --no-dev

# Run with Gunicorn
uv run gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

### 3. Frontend

```bash
cd frontend

# Build for production
npm run build

# Output: frontend/dist/
# Serve with Nginx, Apache, or any static file server
```

### 4. Nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend static files
    location / {
        root /var/www/citypulse/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # API proxy
    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # File upload size
    client_max_body_size 20M;
}
```

---

## Docker (Future)

Docker setup is not yet implemented. Recommended structure:

```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: citypulse
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      SQLALCHEMY_DATABASE_URI: postgresql://postgres:password@db:5432/citypulse
      SECRET_KEY: ${SECRET_KEY}
      JWT_SECRET_KEY: ${JWT_SECRET_KEY}
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  pgdata:
```

---

## Security Checklist for Production

- [ ] Move S3 credentials to environment variables
- [ ] Restrict CORS origins to your domain
- [ ] Use strong, unique `SECRET_KEY` and `JWT_SECRET_KEY`
- [ ] Enable HTTPS (SSL/TLS)
- [ ] Set `FLASK_ENV=production` (disables debug mode)
- [ ] Configure proper database connection pooling
- [ ] Set up database backups
- [ ] Add rate limiting to API endpoints
- [ ] Review and restrict file upload types
- [ ] Set up monitoring and logging

---

## Troubleshooting

### Common Issues

**1. Database connection refused**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check database exists
psql -U postgres -c "\l"
```

**2. S3 upload fails**
```bash
# Test S3 connectivity
aws s3 ls s3://citypulse --endpoint-url https://us-003.s3.synologyc2.net
```

**3. Frontend can't reach API**
```bash
# Check backend is running
curl http://localhost:5000/ping

# Check Vite proxy config
cat frontend/vite.config.js
```

**4. JWT token expired**
```bash
# Tokens expire after 7 days
# Use POST /api/auth/refresh to get new token
curl -X POST http://localhost:5000/api/auth/refresh \
  -H "Authorization: Bearer <refresh_token>"
```
