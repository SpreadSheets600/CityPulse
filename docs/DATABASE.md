# CityPulse Database Schema

## Overview

CityPulse uses **PostgreSQL** as its primary database with **SQLAlchemy ORM** for data access. Migrations are managed via **Flask-Migrate** (Alembic).

---

## Entity Relationship Diagram

```
┌──────────────┐       ┌──────────────────┐       ┌──────────────┐
│    users      │       │     issues       │       │ departments  │
├──────────────┤       ├──────────────────┤       ├──────────────┤
│ id (PK)      │◄──┐   │ id (PK)          │   ┌──►│ id (PK)      │
│ firstname    │   │   │ title            │   │   │ name         │
│ lastname     │   │   │ description      │   │   │ description  │
│ address      │   │   │ image_urls (JSON)│   │   │ contact_email│
│ role (enum)  │   │   │ voice_note_url   │   │   │ contact_phone│
│ phone        │   │   │ video_note_url   │   │   │ created_at   │
│ email        │   │   │ issue_type       │   │   │ updated_at   │
│ password_hash│   │   │ status (enum)    │   │   └──────────────┘
│ profile_pic  │   │   │ latitude         │   │
│ created_at   │   │   │ longitude        │   │
└──────────────┘   │   │ address          │   │
                   │   │ department_id(FK)│───┘
                   │   │ citizen_id (FK)  │───┘
                   │   │ created_at       │
                   │   │ updated_at       │
                   │   └──────────────────┘
                   │            │
                   │            │ 1:N
                   │            ▼
                   │   ┌──────────────────┐
                   │   │ issue_updates    │
                   │   ├──────────────────┤
                   │   │ id (PK)          │
                   │   │ issue_id (FK)    │
                   │   │ author_id (FK)   │
                   │   │ title            │
                   │   │ body             │
                   │   │ progress         │
                   │   │ image_urls (JSON)│
                   │   │ created_at       │
                   │   └──────────────────┘
                   │
                   │   ┌──────────────────┐
                   │   │verification_stat │
                   │   ├──────────────────┤
                   │   │ id (PK)          │
                   │   │ issue_id (FK)    │
                   │   │ status (enum)    │
                   │   │ verified_by (FK) │
                   │   │ verified_at      │
                   │   │ notes            │
                   │   └──────────────────┘
                   │
                   └─── issues.citizen_id → users.id
                        issue_updates.author_id → users.id
                        verification_stat.verified_by → users.id
```

---

## Models

### User

**Table:** `users`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PK, Auto-increment | Unique user ID |
| `firstname` | String(80) | Unique, Not Null | First name |
| `lastname` | String(80) | Unique, Not Null | Last name |
| `address` | String(200) | Not Null | Street address |
| `role` | Enum | Not Null, Default: `citizen` | User role (`citizen` or `admin`) |
| `phone` | String(15) | Unique, Not Null | Phone number |
| `email` | String(120) | Unique, Not Null | Email address |
| `password_hash` | String(120) | Not Null | bcrypt hashed password |
| `profile_picture` | String(200) | Nullable | DiceBear avatar URL |
| `created_at` | DateTime | Default: `datetime.utcnow` | Account creation time |

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
| `issue_type` | String(50) | Default: `"Unspecified"` | Issue category |
| `status` | Enum | Default: `pending` | Current status |
| `latitude` | Float | Not Null | Location latitude |
| `longitude` | Float | Not Null | Location longitude |
| `address` | String(200) | Nullable | Street address |
| `department_id` | Integer | FK → `departments.id`, Nullable | Assigned department |
| `citizen_id` | Integer | FK → `users.id`, Not Null | Reporter |
| `created_at` | DateTime | Default: `datetime.utcnow` | Report time |
| `updated_at` | DateTime | On update: `datetime.utcnow` | Last update time |

**Status Enum Values:**
- `pending` — New issue, awaiting review
- `in_progress` — Being worked on
- `resolved` — Issue fixed
- `rejected` — Issue rejected
- `verified` — Resolution verified

**Issue Type Values:**
- `Pothole`
- `Street Light`
- `Water Supply`
- `Sewage`
- `Garbage`
- `Traffic`
- `Other`
- `Unspecified` (default)

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
| `created_at` | DateTime | Default: `datetime.utcnow` | Update time |

**Relationships:**
- `issue` → Many-to-one with `Issue`
- `author` → Many-to-one with `User`

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
| `created_at` | DateTime | Default: `datetime.utcnow` | Creation time |
| `updated_at` | DateTime | On update: `datetime.utcnow` | Last update time |

**Relationships:**
- `issues` → One-to-many with `Issue`

---

### VerificationStatus

**Table:** `verification_statuses`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | PK, Auto-increment | Unique verification ID |
| `issue_id` | Integer | FK → `issues.id`, Not Null | Verified issue |
| `status` | Enum | Default: `pending` | Verification status |
| `verified_by` | Integer | FK → `users.id`, Nullable | Verifier |
| `verified_at` | DateTime | Nullable | Verification time |
| `notes` | Text | Nullable | Verification notes |

**Status Enum Values:**
- `pending` — Not yet verified
- `verified` — Issue verified
- `rejected` — Verification rejected

---

## Default Data

### Admin Account (Seeded on First Run)

```
Email:    admin@citypulse.com
Password: admin123
Role:     admin
```

---

## Configuration

**Database URL (from `config.py`):**
```python
# PostgreSQL (production)
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@localhost:5432/mydatabase"

# SQLite (fallback)
SQLALCHEMY_DATABASE_URI = "sqlite:///citypulse.db"
```

**Recommended Production Settings:**
```python
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": True,      # Verify connections before use
    "pool_recycle": 300,        # Recycle connections every 5 min
    "pool_size": 10,            # Connection pool size
    "max_overflow": 20,         # Extra connections beyond pool_size
}
```
