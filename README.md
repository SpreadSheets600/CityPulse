# CityPulse

A civic issue reporting and management platform that empowers citizens to report urban problems and enables administrators to track and resolve them efficiently.

---

## Features

### For Citizens

- **Report Issues** — Report potholes, broken street lights, water supply issues, sewage problems, garbage, and traffic issues
- **Rich Media** — Capture photos, record voice notes, and take videos directly from your browser
- **Smart Location** — Use GPS, interactive map, or address search to pinpoint issue locations
- **Track Progress** — Monitor the status of your reported issues with real-time updates
- **Public Dashboard** — View nearby issues on an interactive map

### For Administrators

- **Admin Dashboard** — Overview of all issues with stats and interactive maps
- **Issue Management** — Update status, assign departments, and post progress updates
- **Department Management** — Create and manage departments for issue routing
- **User Management** — View and manage citizen accounts

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Vue 3, Vite 7, Tailwind CSS 4, DaisyUI 5, Pinia, Leaflet |
| **Backend** | Python 3.13, Flask 3.1, Flask-RESTful, SQLAlchemy, Flask-JWT-Extended |
| **Database** | PostgreSQL (SQLite for development) |
| **Storage** | Synology C2 S3 (image/audio/video storage) |
| **Geocoding** | Nominatim (OpenStreetMap) |

---

## Getting Started

### Prerequisites

- Python 3.13+
- Node.js 18+
- PostgreSQL 14+ (or use SQLite for dev)
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

The frontend dev server proxies `/api` requests to the backend automatically.

### Default Admin Account

| Field | Value |
|-------|-------|
| Email | `admin@citypulse.com` |
| Password | `admin123` |

---

## Project Structure

```
CityPulse/
├── backend/                    # Flask REST API
│   ├── api/
│   │   ├── models/            # SQLAlchemy ORM models
│   │   ├── routes/            # API endpoint resources
│   │   └── utils/             # S3 uploads, image compression
│   ├── app.py                 # Flask app factory
│   ├── config.py              # Configuration
│   └── pyproject.toml         # Python dependencies
├── frontend/                  # Vue 3 SPA
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── views/             # Page components
│   │   ├── router/            # Vue Router
│   │   ├── stores/            # Pinia state management
│   │   └── api/               # Axios HTTP client
│   └── package.json
├── devserver.sh               # Dev startup script
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

### Issues

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/issues/report` | Report new issue |
| GET | `/api/issues` | Get all issues |
| GET | `/api/issues/public` | Get public issues |
| GET | `/api/issues/my-issues` | Get user's issues |
| GET | `/api/issues/:id` | Get issue detail |
| PUT | `/api/issues/:id` | Add images to issue |

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
| [Contributing](docs/CONTRIBUTING.md) | Contribution guidelines |
| [Security](docs/SECURITY.md) | Security measures and recommendations |
