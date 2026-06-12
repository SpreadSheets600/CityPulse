# CityPulse Architecture

## Overview

CityPulse is a **civic issue reporting and management platform** built as a monorepo with two independent applications: a Python/Flask REST API backend and a Vue 3 Single Page Application (SPA) frontend.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      CLIENTS                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │  Web Browser │  │  Mobile Web │  │  Admin Panel │    │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘    │
└─────────┼────────────────┼────────────────┼─────────────┘
          │                │                │
          ▼                ▼                ▼
┌─────────────────────────────────────────────────────────┐
│                   VITE DEV SERVER                        │
│              (Frontend SPA + API Proxy)                   │
│                  Port: 5173                              │
└────────────────────────┬────────────────────────────────┘
                         │  /api/*
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  FLASK REST API                          │
│                  Port: 5000                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │   Auth    │  │  Issues  │  │  Admin   │              │
│  │  Routes   │  │  Routes  │  │  Routes  │              │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘              │
│       │              │              │                     │
│  ┌────▼──────────────▼──────────────▼─────┐              │
│  │           SQLAlchemy ORM                │              │
│  └────────────────┬───────────────────────┘              │
└───────────────────┼──────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│PostgreSQL│ │  S3 C2   │ │Nominatim │
│ Database │ │ Storage  │ │Geocoding │
└──────────┘ └──────────┘ └──────────┘
```

---

## Project Structure

```
CityPulse/
├── backend/                    # Python/Flask REST API
│   ├── api/
│   │   ├── models/            # SQLAlchemy ORM models
│   │   │   ├── user.py        # User model with roles
│   │   │   ├── issue.py       # Issue model with status tracking
│   │   │   ├── department.py  # Department model
│   │   │   ├── issue_update.py# Issue update/progress tracking
│   │   │   └── verification.py# Verification status model
│   │   ├── routes/            # Flask-RESTful Resource classes
│   │   │   ├── auth.py        # Authentication endpoints
│   │   │   ├── issues.py      # Issue CRUD + geocoding
│   │   │   ├── admin.py       # Admin management endpoints
│   │   │   └── users.py       # (Unused) mock user route
│   │   └── utils/
│   │       └── s3.py          # S3 upload + image compression
│   ├── app.py                 # Flask app factory + route registration
│   ├── config.py              # Configuration (DB, JWT, S3)
│   ├── pyproject.toml         # Python dependencies (uv)
│   └── .env.example           # Environment variable template
├── frontend/                  # Vue 3 SPA
│   ├── src/
│   │   ├── api/
│   │   │   └── client.js      # Axios instance with interceptors
│   │   ├── components/        # Reusable UI components
│   │   │   ├── App-Navbar.vue
│   │   │   ├── Auth-Login.vue
│   │   │   ├── Auth-Register.vue
│   │   │   ├── Issue-Form.vue
│   │   │   ├── Location-Selector.vue
│   │   │   ├── Photo-Capture-Modal.vue
│   │   │   ├── Audio-Capture-Modal.vue
│   │   │   ├── Video-Capture-Modal.vue
│   │   │   └── ImageLightbox.vue
│   │   ├── views/             # Page-level components
│   │   │   ├── Public-Landing.vue
│   │   │   ├── User-Dashboard.vue
│   │   │   ├── User-Issues.vue
│   │   │   ├── Issue-Create.vue
│   │   │   ├── Issue-Detail.vue
│   │   │   ├── User-Profile.vue
│   │   │   ├── Admin-Dashboard.vue
│   │   │   └── Admin-Issue-Manage.vue
│   │   ├── router/
│   │   │   └── index.js       # Vue Router with navigation guards
│   │   ├── stores/
│   │   │   └── auth.js        # Pinia auth store
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
├── devserver.sh               # Dev startup script (both servers)
├── .prettierrc.json
├── .editorconfig
└── .gitignore
```

---

## Backend Architecture

### Framework: Flask + Flask-RESTful

The backend uses a **resource-based architecture** where each API endpoint is a Flask-RESTful `Resource` class with HTTP method handlers (`get()`, `post()`, `put()`, `delete()`).

**Request Flow:**
```
HTTP Request
    │
    ▼
Flask App (app.py)
    │
    ├── CORS Middleware
    ├── JWT Middleware (if protected route)
    │
    ▼
Route Registration (add_resource)
    │
    ▼
Resource Class (e.g., IssueListResource)
    │
    ├── Parse/Validate Input
    ├── Query Database (SQLAlchemy)
    ├── Process Business Logic
    └── Return JSON Response
```

### Key Patterns

| Pattern | Implementation |
|---------|---------------|
| **App Factory** | `create_app()` in `app.py` builds and configures Flask |
| **Resource Classes** | Each endpoint = a class with HTTP method handlers |
| **Model Layer** | SQLAlchemy ORM models with relationships |
| **Utils Layer** | S3 uploads, image compression isolated in `utils/` |
| **Middleware** | JWT auth, CORS applied at app level |

---

## Frontend Architecture

### Framework: Vue 3 + Composition API

The frontend uses a **component-based architecture** with Vue 3's Composition API (`<script setup>` syntax).

**Data Flow:**
```
User Interaction
    │
    ▼
View Component (e.g., User-Dashboard.vue)
    │
    ├── Calls API (via axios client)
    │       │
    │       ▼
    │   Axios Interceptor
    │       ├── Injects JWT token
    │       └── Handles 401 → redirect to /login
    │
    ├── Response → Update reactive state
    │
    ▼
Template Renders (reactive data binding)
```

### Key Patterns

| Pattern | Implementation |
|---------|---------------|
| **Composition API** | `<script setup>` for all components |
| **State Management** | Pinia store for auth state |
| **Route Guards** | Navigation guards for auth/admin checks |
| **Axios Interceptors** | Token injection + error handling |
| **Component Composition** | Views compose multiple child components |
| **Global Components** | `ImageLightbox` registered globally |

---

## Authentication & Authorization

### JWT-Based Authentication

```
Registration/Login
    │
    ▼
POST /api/auth/login
    │
    ├── Verify credentials (bcrypt)
    ├── Generate JWT access token (7-day expiry)
    └── Return token + user data
         │
         ▼
Frontend stores token in localStorage
    │
    ▼
Subsequent Requests
    │
    ├── Axios interceptor adds: Authorization: Bearer <token>
    │
    ▼
Backend JWT Middleware
    ├── Validates token
    ├── Extracts user_id
    └── Attaches to request context
         │
         ▼
Route Handler
    └── Access current_user via get_jwt_identity()
```

### Role-Based Access Control

| Role | Permissions |
|------|------------|
| `citizen` | Report issues, view own issues, view public issues |
| `admin` | All citizen permissions + manage all users, update issue status, assign departments, post updates |

**Admin Route Protection:**
- Backend: Each admin endpoint checks `user.role != UserRole.admin` → returns 403
- Frontend: Router guard checks `authStore.user?.role !== 'admin'` → redirects to `/dashboard`

---

## Data Flow

### Issue Reporting Flow

```
Citizen fills form (title, description, type, location, media)
    │
    ▼
POST /api/issues/report (multipart/form-data)
    │
    ├── Validate inputs
    ├── Geocode address (if provided) → lat/lng
    ├── Upload images to S3 → compress to WEBP → get presigned URLs
    ├── Upload voice note to S3 → get presigned URL
    ├── Upload video note to S3 → get presigned URL
    ├── Create Issue record in database
    └── Return issue data
```

### Issue Resolution Flow

```
Admin views issue in dashboard
    │
    ▼
Admin-Issue-Manage.vue
    │
    ├── Updates status (pending → in_progress → resolved)
    ├── Assigns department
    ├── Posts update with progress %
    └── Attaches images to update
         │
         ▼
PUT/POST /api/admin/issues/<id>/status|department|updates
    │
    ├── Update Issue record
    ├── Create IssueUpdate record
    └── Return updated data
```

---

## External Services

| Service | Purpose | Integration |
|---------|---------|-------------|
| **PostgreSQL** | Primary database | SQLAlchemy ORM |
| **Synology C2 S3** | Image/voice/video storage | boto3 client |
| **Nominatim** | Address geocoding | HTTP API (no library) |
| **DiceBear** | Profile picture generation | External URL (no backend call) |
| **Vite** | Frontend dev/build | Dev server + API proxy |

---

## Security Considerations

| Area | Implementation |
|------|---------------|
| Password Storage | bcrypt hashing via passlib |
| JWT Tokens | 7-day expiry, header-based |
| CORS | Currently allows all origins (permissive) |
| S3 Access | Presigned URLs with 7-day expiry |
| Input Validation | Server-side via Flask-RESTful |
| SQL Injection | Prevented by SQLAlchemy ORM |

**Known Issues:**
- S3 credentials hardcoded in `config.py` (should use env vars)
- CORS allows all origins (should restrict in production)
- No rate limiting on endpoints
- No CSRF protection on state-changing endpoints
