# CityPulse Architecture

## Overview

CityPulse is a **civic issue reporting and management platform** built as a monorepo with two independent applications: a Python/Flask REST API backend and a Vue 3 Single Page Application (SPA) frontend.

## High-Level Architecture

```mermaid
graph TB
    subgraph Clients["CLIENTS"]
        WB[Web Browser]
        MW[Mobile Web]
        AP[Admin Panel]
    end

    subgraph Frontend["FRONTEND - Vite Dev Server (Port 5173)"]
        VDS[Vite Dev Server<br/>SPA + API Proxy]
    end

    subgraph Backend["BACKEND - Flask REST API (Port 5000)"]
        AR[Auth Routes]
        IR[Issues Routes]
        ADR[Admin Routes]
        ORM[SQLAlchemy ORM]
        AR & IR & ADR --> ORM
    end

    subgraph Services["EXTERNAL SERVICES"]
        PG[(PostgreSQL Database)]
        S3[(Synology C2 S3<br/>Media Storage)]
        NOM[Nominatim<br/>Geocoding]
    end

    WB --> VDS
    MW --> VDS
    AP --> VDS
    VDS -->|/api/*| Backend
    ORM --> PG
    ORM --> S3
    ORM --> NOM
```

## Project Structure

```
CityPulse/
├── backend/                    # Python/Flask REST API
│   ├── api/
│   │   ├── models/             # SQLAlchemy ORM models
│   │   │   ├── user.py         # User model with roles
│   │   │   ├── issue.py        # Issue model with status tracking
│   │   │   ├── department.py   # Department model (with SLA)
│   │   │   ├── issue_update.py # Issue update/progress tracking
│   │   │   ├── verification.py # Verification status model
│   │   │   ├── upvote.py       # Citizen upvotes
│   │   │   ├── comment.py      # Issue comments
│   │   │   ├── audit_log.py    # Admin action audit trail
│   │   │   ├── geofence.py     # Geographic bounding boxes
│   │   │   └── password_reset.py # Password reset tokens
│   │   ├── routes/             # Flask-RESTful Resource classes
│   │   │   ├── auth.py         # Authentication endpoints
│   │   │   ├── issues.py       # Issue CRUD + geocoding + AI
│   │   │   ├── admin.py        # Admin management endpoints
│   │   │   ├── oauth.py        # Google/GitHub OAuth2
│   │   │   └── chatbot.py      # AI chatbot endpoint
│   │   ├── data/
│   │   │   └── departments.json # Default department seed data
│   │   └── utils/
│   │       ├── s3.py           # S3 upload + image compression
│   │       ├── email.py        # Flask-Mail notifications
│   │       ├── sms.py          # Twilio SMS notifications
│   │       ├── classifier.py   # AI issue classification
│   │       ├── duplicate_detector.py # Duplicate detection
│   │       └── priority_scorer.py   # Priority scoring
│   ├── tests/                  # pytest test suite
│   ├── app.py                  # Flask app factory + route registration
│   ├── config.py               # Configuration (DB, JWT, S3, OAuth)
│   ├── Dockerfile              # Python 3.13 + gunicorn
│   ├── pyproject.toml          # Python dependencies (uv)
│   └── .env.example            # Environment variable template
├── frontend/                   # Vue 3 SPA
│   ├── src/
│   │   ├── api/client.js       # Axios instance with interceptors
│   │   ├── components/         # Reusable UI components
│   │   ├── views/              # Page-level components
│   │   ├── router/index.js     # Vue Router with navigation guards
│   │   ├── stores/             # Pinia stores (auth, chatbot)
│   │   ├── App.vue
│   │   └── main.js
│   ├── Dockerfile              # Multi-stage Node build + nginx
│   └── nginx.conf              # Reverse proxy config
├── docker-compose.yml          # Docker Compose orchestration
├── devserver.sh                # Dev startup script (both servers)
└── .github/workflows/ci.yml    # CI/CD pipeline
```

## Backend Architecture

The backend uses a **resource-based architecture** where each API endpoint is a Flask-RESTful `Resource` class with HTTP method handlers.

```mermaid
flowchart LR
    A[HTTP Request] --> B[Flask App]
    B --> C{CORS & JWT<br/>Middleware}
    C --> D[Route Registration]
    D --> E[Resource Class]
    E --> F[Parse / Validate Input]
    F --> G[SQLAlchemy Query]
    G --> H[Business Logic]
    H --> I[JSON Response]
```

### Key Patterns

| Pattern | Implementation |
|---------|---------------|
| **App Factory** | `create_app()` builds and configures Flask |
| **Resource Classes** | Each endpoint = a class with HTTP method handlers |
| **Model Layer** | SQLAlchemy ORM models with relationships |
| **Utils Layer** | S3 uploads, email, SMS, AI classification isolated in `utils/` |
| **Middleware** | JWT auth, CORS, rate limiting applied at app level |
| **AI Pipeline** | Classification → Duplicate Detection → Priority Scoring |

## Frontend Architecture

The frontend uses a **component-based architecture** with Vue 3's Composition API (`<script setup>` syntax).

```mermaid
flowchart LR
    A[User Interaction] --> B[View Component]
    B --> C[Axios API Call]
    C --> D{Axios Interceptor}
    D --> E[Inject JWT Token]
    D --> F[Handle 401 → /login]
    C --> G[Update Reactive State]
    G --> H[Template Renders]
```

### Key Patterns

| Pattern | Implementation |
|---------|---------------|
| **Composition API** | `<script setup>` for all components |
| **State Management** | Pinia store for auth state |
| **Route Guards** | Navigation guards for auth/admin checks |
| **Axios Interceptors** | Token injection + error handling |
| **Component Composition** | Views compose multiple child components |

## Authentication & Authorization

### JWT-Based Authentication Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant F as Frontend
    participant B as Backend API
    participant D as Database

    C->>F: Enter credentials
    F->>B: POST /api/auth/login
    B->>D: Verify credentials (bcrypt)
    D-->>B: User found
    B->>B: Generate JWT (7-day expiry)
    B-->>F: { access_token, user }
    F->>F: Store token in localStorage
    Note over F,B: Subsequent requests
    C->>F: Make request
    F->>F: Axios interceptor adds<br/>Authorization: Bearer
    F->>B: API call with token
    B->>B: Validate JWT
    B-->>F: Response
    F-->>C: Render data
```

### Role-Based Access Control

| Role | Permissions |
|------|-------------|
| `citizen` | Report issues, view own issues, view public issues |
| `admin` | All citizen permissions + manage users, update issue status, assign departments, post updates |

**Admin Route Protection:**
- Backend: Each admin endpoint checks `user.role != UserRole.admin` → returns 403
- Frontend: Router guard checks `authStore.user?.role !== 'admin'` → redirects to `/dashboard`

## Data Flow

### Issue Reporting Flow

```mermaid
flowchart TD
    A[Citizen fills form] --> B[POST /api/issues/report]
    B --> C[Validate inputs]
    C --> D{Has address?}
    D -->|Yes| E[Geocode → lat/lng]
    D -->|No| F[Skip geocoding]
    E --> G[Upload media to S3]
    F --> G
    G --> H[Compress images to WEBP]
    H --> I[Generate presigned URLs]
    I --> J[Create Issue record in DB]
    J --> K[Run AI pipeline]
    K --> L[Return issue + AI data]
```

### Issue Resolution Flow

```mermaid
flowchart TD
    A[Admin views issue] --> B[Admin-Issue-Manage.vue]
    B --> C{Action}
    C -->|Update Status| D[PUT /api/admin/issues/id/status]
    C -->|Assign Department| E[PUT /api/admin/issues/id/department]
    C -->|Post Update| F[POST /api/admin/issues/id/updates]
    D & E & F --> G[Update DB records]
    G --> H[Return updated data]
```

## External Services

| Service | Purpose | Integration |
|---------|---------|-------------|
| **PostgreSQL** | Primary database | SQLAlchemy ORM |
| **Synology C2 S3** | Image/voice/video storage | boto3 client |
| **Nominatim** | Address geocoding | HTTP API |
| **DiceBear** | Profile picture generation | External URL |
| **Twilio** | SMS notifications | twilio Python client |
| **Flask-Mail** | Email notifications | SMTP integration |
| **Authlib** | OAuth2 (Google/GitHub) | OAuth2 client |
| **Vite** | Frontend dev/build | Dev server + API proxy |

## Security Considerations

| Area | Implementation |
|------|---------------|
| Password Storage | bcrypt hashing via passlib |
| JWT Tokens | 7-day expiry, header-based |
| CORS | Configurable via `CORS_ORIGINS` env var |
| S3 Access | Presigned URLs with 7-day expiry |
| Input Validation | Server-side via Flask-RESTful |
| SQL Injection | Prevented by SQLAlchemy ORM |
| Rate Limiting | Flask-Limiter on auth endpoints |
| OAuth2 | Authlib for Google/GitHub SSO |
