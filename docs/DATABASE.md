# CityPulse Database Schema

## Overview

CityPulse uses **PostgreSQL** as its primary database with **SQLAlchemy ORM** for data access. Migrations are managed via **Flask-Migrate** (Alembic).

## Entity Relationship Diagram

```mermaid
erDiagram
    users ||--o{ issues : "citizen reports"
    users ||--o{ issue_updates : "author writes"
    users ||--o{ verification_statuses : "verifier"
    departments ||--o{ issues : "assigned to"
    issues ||--o{ issue_updates : "has updates"
    issues ||--o| verification_statuses : "has verification"

    users {
        int id PK
        string firstname
        string lastname
        string address
        enum role "citizen | admin"
        string phone UK
        string email UK
        string password_hash
        string profile_picture "nullable"
        datetime created_at
    }

    issues {
        int id PK
        string title
        string description
        json image_urls
        string voice_note_url "nullable"
        string video_note_url "nullable"
        string issue_type
        enum status "pending | in_progress | resolved | rejected | verified"
        float latitude
        float longitude
        string address "nullable"
        int department_id FK "nullable"
        int citizen_id FK
        datetime created_at
        datetime updated_at
    }

    departments {
        int id PK
        string name UK
        string description "nullable"
        string contact_email UK
        string contact_phone UK
        datetime created_at
        datetime updated_at
    }

    issue_updates {
        int id PK
        int issue_id FK
        int author_id FK
        string title
        text body "nullable"
        int progress "0-100"
        json image_urls
        datetime created_at
    }

    verification_statuses {
        int id PK
        int issue_id FK
        enum status "pending | verified | rejected"
        int verified_by FK "nullable"
        datetime verified_at "nullable"
        text notes "nullable"
    }
```

## Models

### User

**Table:** `users`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PK, Auto-increment | Unique user ID |
| `firstname` | String(80) | Unique, Not Null | First name |
| `lastname` | String(80) | Unique, Not Null | Last name |
| `address` | String(200) | Not Null | Street address |
| `role` | Enum | Not Null, Default: `citizen` | `citizen` or `admin` |
| `phone` | String(15) | Unique, Not Null | Phone number |
| `email` | String(120) | Unique, Not Null | Email address |
| `password_hash` | String(120) | Not Null | bcrypt hashed password |
| `profile_picture` | String(200) | Nullable | DiceBear avatar URL |
| `created_at` | DateTime | Default: `utcnow` | Account creation time |

**Relationships:**

- `issues` → One-to-many with `Issue` (via `citizen_id`)

---

### Issue

**Table:** `issues`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PK, Auto-increment | Unique issue ID |
| `title` | String(100) | Not Null | Issue title |
| `description` | String(500) | Not Null | Issue description |
| `image_urls` | JSON | Not Null | Array of S3 presigned URLs |
| `voice_note_url` | String | Nullable | S3 presigned URL for audio |
| `video_note_url` | String | Nullable | S3 presigned URL for video |
| `issue_type` | String(50) | Default: `Unspecified` | Issue category |
| `status` | Enum | Default: `pending` | Current status |
| `latitude` | Float | Not Null | Location latitude |
| `longitude` | Float | Not Null | Location longitude |
| `address` | String(200) | Nullable | Street address |
| `department_id` | Integer | FK → `departments.id`, Nullable | Assigned department |
| `citizen_id` | Integer | FK → `users.id`, Not Null | Reporter |
| `created_at` | DateTime | Default: `utcnow` | Report time |
| `updated_at` | DateTime | On update: `utcnow` | Last update time |

**Status Enum Values:**

- `pending` — New issue, awaiting review
- `in_progress` — Being worked on
- `resolved` — Issue fixed
- `rejected` — Issue rejected
- `verified` — Resolution verified

**Issue Type Values:**

- `Pothole`, `Street Light`, `Water Supply`, `Sewage`, `Garbage`, `Traffic`, `Other`, `Unspecified` (default)

**Relationships:**

- `citizen` → Many-to-one with `User`
- `department` → Many-to-one with `Department`
- `verification` → One-to-one with `VerificationStatus`
- `updates` → One-to-many with `IssueUpdate` (cascade delete)

---

### IssueUpdate

**Table:** `issue_updates`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PK, Auto-increment | Unique update ID |
| `issue_id` | Integer | FK → `issues.id`, Not Null | Parent issue |
| `author_id` | Integer | FK → `users.id`, Not Null | Update author (admin) |
| `title` | String(120) | Not Null | Update title |
| `body` | Text | Nullable | Update description |
| `progress` | Integer | Default: 0 | Progress percentage (0-100) |
| `image_urls` | JSON | Default: `[]` | Array of S3 presigned URLs |
| `created_at` | DateTime | Default: `utcnow` | Update time |

---

### Department

**Table:** `departments`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PK, Auto-increment | Unique department ID |
| `name` | String(100) | Unique, Not Null | Department name |
| `description` | String(500) | Nullable | Department description |
| `contact_email` | String(120) | Unique, Not Null | Contact email |
| `contact_phone` | String(15) | Unique, Not Null | Contact phone |
| `created_at` | DateTime | Default: `utcnow` | Creation time |
| `updated_at` | DateTime | On update: `utcnow` | Last update time |

---

### VerificationStatus

**Table:** `verification_statuses`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PK, Auto-increment | Unique verification ID |
| `issue_id` | Integer | FK → `issues.id`, Not Null | Verified issue |
| `status` | Enum | Default: `pending` | `pending`, `verified`, or `rejected` |
| `verified_by` | Integer | FK → `users.id`, Nullable | Verifier |
| `verified_at` | DateTime | Nullable | Verification time |
| `notes` | Text | Nullable | Verification notes |

---

## Default Data

### Admin Account (Seeded on First Run)

| Field | Value |
|-------|-------|
| Email | `admin@citypulse.com` |
| Password | `admin123` |
| Role | `admin` |

### Departments (Loaded from `backend/api/data/departments.json`)

| Department | Contact |
|------------|---------|
| Electricity | <electricity@citypulse.com> |
| Water Supply | <water@citypulse.com> |
| Waste Management | <waste@citypulse.com> |
| Public Transportation | <publictransport@citypulse.com> |
| Road Maintenance | <roads@citypulse.com> |

## Configuration

**Database URL (from `config.py`):**

```python
# PostgreSQL (production)
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@localhost:5432/mydatabase"

# SQLite (fallback)
SQLALCHEMY_DATABASE_URI = "sqlite:///citypulse.db"
```

**Production Settings:**

```python
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
    "pool_size": 10,
    "max_overflow": 20,
}
```
