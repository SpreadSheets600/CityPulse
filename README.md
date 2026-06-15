# CityPulse

A civic issue reporting and management platform that empowers citizens to report urban problems and enables administrators to track and resolve them efficiently. Features AI-powered classification, duplicate detection, priority scoring, and a chatbot assistant.

---

## Features

### For Citizens

- **Report Issues** — Report potholes, broken street lights, water supply issues, sewage problems, garbage, and traffic issues
- **Rich Media** — Capture photos, record voice notes, and take videos directly from your browser
- **Smart Location** — Use GPS, interactive map, or address search to pinpoint issue locations
- **Track Progress** — Monitor the status of your reported issues with real-time updates
- **Public Dashboard** — View nearby issues on an interactive map
- **Upvoting** — Show support for issues that matter to you
- **Comments** — Add additional information to issues
- **AI Chatbot** — Get instant help with reporting and tracking issues

### For Administrators

- **Admin Dashboard** — Overview of all issues with stats and interactive maps
- **Issue Management** — Update status, assign departments, and post progress updates
- **Department Management** — Create and manage departments for issue routing
- **User Management** — View and manage citizen accounts
- **Analytics Dashboard** — Charts, trends, and resolution time metrics
- **CSV Export** — Export issues data with filters
- **SLA Tracking** — Monitor resolution time against targets
- **Geofencing** — Auto-assign issues by location
- **Audit Log** — Track all admin actions

### AI Intelligence

- **Auto-Classification** — Issues automatically categorized from text analysis
- **Duplicate Detection** — Identifies similar reported issues to prevent duplicates
- **Priority Scoring** — Multi-factor urgency ranking (text analysis, upvotes, age, type)

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Vue 3, Vite 7, Tailwind CSS 4, DaisyUI 5, Pinia, Leaflet, Chart.js |
| **Backend** | Python 3.13, Flask 3.1, Flask-RESTful, SQLAlchemy, Flask-JWT-Extended |
| **Database** | SQLite |
| **Storage** | Synology C2 S3 (image/audio/video storage) |
| **Geocoding** | Nominatim (OpenStreetMap) |
| **Auth** | JWT (Flask-JWT-Extended) |
| **Notifications** | Flask-Mail (email), Twilio (SMS) |
| **Testing** | pytest (backend), Vitest (frontend) |
| **DevOps** | Docker, Docker Compose, GitHub Actions CI/CD |

---

## Getting Started

### Prerequisites

- Python 3.13+
- Node.js 18+
- [uv](https://docs.astral.sh/uv/) (Python package manager)

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd CityPulse
```

**Backend:**

```bash
cd backend
uv sync
cp .env.example .env
# Edit .env with your database credentials
uv run flask db upgrade
```

**Frontend:**

```bash
cd frontend
npm install
```

### Running

**Option 1 — Run both servers:**

```bash
chmod +x devserver.sh
./devserver.sh
```

**Option 2 — Run separately:**

```bash
# Terminal 1 — Backend (port 5000)
cd backend && uv run flask run --debug

# Terminal 2 — Frontend (port 5173)
cd frontend && npm run dev
```

**Option 3 — Docker Compose:**

```bash
docker compose up -d
```

The frontend dev server proxies `/api` requests to the backend automatically.

### Default Admin Account

| Field | Value |
|-------|-------|
| Email | `admin@citypulse.com` |
| Password | `admin123` |

---

## Testing

```bash
# Backend tests
cd backend
PYTHONPATH=. uv run pytest tests/ -v

# Frontend tests
cd frontend
npx vitest run
```

---

## Project Structure

```
CityPulse/
├── backend/                    # Flask REST API
│   ├── api/
│   │   ├── models/            # SQLAlchemy ORM models
│   │   ├── routes/            # API endpoint resources
│   │   ├── utils/             # S3, email, SMS, AI classification
│   │   └── data/              # Seed data (departments)
│   ├── app.py                 # Flask app factory
│   ├── config.py              # Configuration
│   ├── Dockerfile             # Python 3.13 + gunicorn
│   └── pyproject.toml         # Python dependencies
├── frontend/                  # Vue 3 SPA
│   ├── src/
│   │   ├── components/        # Reusable UI components (12)
│   │   ├── views/             # Page components (17)
│   │   ├── router/            # Vue Router
│   │   ├── stores/            # Pinia state management
│   │   ├── api/               # Axios HTTP client
│   │   └── __tests__/         # Vitest test suite
│   ├── Dockerfile             # Multi-stage Node + nginx
│   ├── nginx.conf             # Reverse proxy config
│   └── package.json
├── docker-compose.yml         # Docker Compose orchestration
├── .github/workflows/ci.yml  # CI/CD pipeline
└── docs/                      # Documentation
```

---

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login (email or phone) |
| POST | `/api/auth/logout` | Logout |
| GET | `/api/auth/me` | Get current user |
| PUT | `/api/auth/profile` | Update profile |
| POST | `/api/auth/forgot-password` | Request password reset |
| POST | `/api/auth/reset-password` | Reset password with token |

### Issues

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/issues/report` | Report new issue (with AI classification) |
| GET | `/api/issues` | Get all issues |
| GET | `/api/issues/public` | Get public issues |
| GET | `/api/issues/my-issues` | Get user's issues |
| GET | `/api/issues/:id` | Get issue detail |
| PUT | `/api/issues/:id` | Add images to issue |
| POST | `/api/issues/:id/upvote` | Upvote an issue |
| GET/POST | `/api/issues/:id/comments` | Get/add comments |

### Admin

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/admin/users` | List all users |
| DELETE | `/api/admin/users/:id` | Delete user |
| GET | `/api/admin/issues` | List all issues |
| PUT | `/api/admin/issues/:id/status` | Update issue status |
| POST | `/api/admin/departments` | Create department |
| PUT | `/api/admin/issues/:id/department` | Assign department |
| POST | `/api/admin/issues/:id/updates` | Post issue update |
| GET | `/api/admin/analytics` | Get analytics data |
| GET | `/api/admin/export` | Export issues CSV |
| GET | `/api/admin/sla` | Get SLA report |
| GET/POST/DELETE | `/api/admin/geofences` | Manage geofences |
| POST | `/api/admin/issues/:id/auto-assign` | Auto-assign by geofence |
| GET | `/api/admin/audit-log` | Get audit log |

### AI

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chatbot` | Chat with AI assistant |

Full API documentation: [docs/API.md](docs/API.md)

---

## Documentation

| Document | Description |
|----------|-------------|
| [Architecture](docs/ARCHITECTURE.md) | System architecture and design patterns |
| [Features](docs/FEATURES.md) | Current features and planned roadmap |
| [API](docs/API.md) | Complete API reference |
| [Database](docs/DATABASE.md) | Schema, models, and relationships |
| [Deployment](docs/DEPLOYMENT.md) | Production deployment guide |
| [Roadmap](docs/ROADMAP.md) | Feature roadmap and technical debt |
| [Security](docs/SECURITY.md) | Security measures and recommendations |
