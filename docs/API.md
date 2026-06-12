# CityPulse API Documentation

## Base URL

```
Development: http://localhost:5000
Production:  https://your-domain.com
```

## Authentication

All protected endpoints require a JWT token in the `Authorization` header:

```
Authorization: Bearer <token>
```

**Obtain a token via:**
- `POST /api/auth/login` — Returns access token
- `POST /api/auth/register` — Returns access token

---

## Authentication Endpoints

### POST `/api/auth/register`

Register a new user account.

**Request Body:**
```json
{
  "firstname": "John",
  "lastname": "Doe",
  "email": "john@example.com",
  "phone": "1234567890",
  "address": "123 Main St, City",
  "password": "securepassword"
}
```

**Response (201):**
```json
{
  "message": "User registered successfully",
  "access_token": "eyJhbGci...",
  "user": {
    "id": 1,
    "firstname": "John",
    "lastname": "Doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "address": "123 Main St, City",
    "role": "citizen",
    "profile_picture": "https://api.dicebear.com/..."
  }
}
```

**Errors:**
- `400` — Missing required fields
- `409` — Email or phone already registered

---

### POST `/api/auth/login`

Login with email or phone number.

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "securepassword"
}
```

OR

```json
{
  "phone": "1234567890",
  "password": "securepassword"
}
```

**Response (200):**
```json
{
  "message": "Login successful",
  "access_token": "eyJhbGci...",
  "user": {
    "id": 1,
    "firstname": "John",
    "lastname": "Doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "role": "citizen",
    "profile_picture": "https://api.dicebear.com/..."
  }
}
```

**Errors:**
- `400` — Missing credentials
- `401` — Invalid credentials

---

### POST `/api/auth/logout`

Logout (clear JWT cookie).

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
{
  "message": "Logged out successfully"
}
```

---

### POST `/api/auth/refresh`

Refresh access token.

**Headers:** `Authorization: Bearer <refresh_token>`

**Response (200):**
```json
{
  "access_token": "eyJhbGci..."
}
```

---

### GET `/api/auth/me`

Get current authenticated user.

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
{
  "id": 1,
  "firstname": "John",
  "lastname": "Doe",
  "email": "john@example.com",
  "phone": "1234567890",
  "address": "123 Main St, City",
  "role": "citizen",
  "profile_picture": "https://api.dicebear.com/...",
  "created_at": "2025-01-15T10:30:00"
}
```

---

## Issue Endpoints

### POST `/api/issues/report`

Report a new issue (multipart/form-data).

**Headers:** `Authorization: Bearer <token>`

**Request Body (multipart/form-data):**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | Yes | Issue title (max 100 chars) |
| `description` | string | Yes | Issue description (max 500 chars) |
| `issue_type` | string | Yes | One of: Pothole, Street Light, Water Supply, Sewage, Garbage, Traffic, Other |
| `latitude` | float | Yes | Location latitude |
| `longitude` | float | Yes | Location longitude |
| `address` | string | No | Street address |
| `images` | file[] | No | Up to 10 images (max 15MB each) |
| `voice_note` | file | No | Audio file for voice note |
| `video_note` | file | No | Video file for video note |

**Response (201):**
```json
{
  "message": "Issue reported successfully",
  "issue": {
    "id": 1,
    "title": "Large pothole on Main St",
    "description": "Deep pothole near the intersection...",
    "issue_type": "Pothole",
    "status": "pending",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "address": "123 Main St, New York, NY",
    "image_urls": ["https://s3...presigned-url"],
    "voice_note_url": null,
    "video_note_url": null,
    "citizen_id": 1,
    "created_at": "2025-01-15T10:30:00"
  }
}
```

**Errors:**
- `400` — Missing required fields
- `413` — File too large (>15MB)

---

### GET `/api/issues`

Get all issues (authenticated).

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
{
  "issues": [
    {
      "id": 1,
      "title": "Large pothole on Main St",
      "description": "...",
      "issue_type": "Pothole",
      "status": "pending",
      "latitude": 40.7128,
      "longitude": -74.0060,
      "address": "123 Main St",
      "image_urls": ["..."],
      "citizen_id": 1,
      "created_at": "2025-01-15T10:30:00",
      "updated_at": "2025-01-15T10:30:00"
    }
  ]
}
```

---

### GET `/api/issues/public`

Get public issues (no auth required).

Returns limited fields (no user data, no media URLs beyond images).

**Query Parameters:** None

**Response (200):**
```json
{
  "issues": [
    {
      "id": 1,
      "title": "Large pothole on Main St",
      "description": "...",
      "issue_type": "Pothole",
      "status": "pending",
      "latitude": 40.7128,
      "longitude": -74.0060,
      "address": "123 Main St",
      "created_at": "2025-01-15T10:30:00"
    }
  ]
}
```

---

### GET `/api/issues/my-issues`

Get current user's issues.

**Headers:** `Authorization: Bearer <token>`

**Response (200):** Same as `GET /api/issues` but filtered to current user.

---

### GET `/api/issues/<id>`

Get single issue detail.

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
{
  "id": 1,
  "title": "Large pothole on Main St",
  "description": "...",
  "issue_type": "Pothole",
  "status": "in_progress",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "address": "123 Main St",
  "image_urls": ["https://s3..."],
  "voice_note_url": "https://s3...",
  "video_note_url": null,
  "citizen_id": 1,
  "department_id": 2,
  "created_at": "2025-01-15T10:30:00",
  "updates": [
    {
      "id": 1,
      "title": "Investigation Started",
      "body": "Team dispatched to inspect...",
      "progress": 25,
      "image_urls": [],
      "created_at": "2025-01-16T09:00:00"
    }
  ]
}
```

---

### PUT `/api/issues/<id>`

Add images to existing issue.

**Headers:** `Authorization: Bearer <token>`

**Request Body (multipart/form-data):**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `images` | file[] | Yes | Additional images (max 15MB each) |

**Response (200):**
```json
{
  "message": "Images added successfully",
  "issue": { ... }
}
```

**Errors:**
- `403` — Not the issue owner
- `404` — Issue not found

---

### GET `/api/issues/<id>/updates`

Get updates for an issue.

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
{
  "updates": [
    {
      "id": 1,
      "title": "Investigation Started",
      "body": "Team dispatched to inspect...",
      "progress": 25,
      "image_urls": [],
      "created_at": "2025-01-16T09:00:00",
      "author": {
        "id": 1,
        "firstname": "Admin",
        "lastname": "User"
      }
    }
  ]
}
```

---

## Geocoding Endpoints

### GET `/api/geocode?q=<address>`

Geocode an address to coordinates.

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `q` | string | Yes | Address to geocode |

**Response (200):**
```json
{
  "suggestions": [
    {
      "display_name": "123 Main St, New York, NY 10001, USA",
      "lat": 40.7128,
      "lon": -74.0060
    }
  ]
}
```

---

### GET `/api/reverse-geocode?lat=<lat>&lon=<lon>`

Reverse geocode coordinates to address.

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `lat` | float | Yes | Latitude |
| `lon` | float | Yes | Longitude |

**Response (200):**
```json
{
  "address": "123 Main St, New York, NY 10001, USA"
}
```

---

## Admin Endpoints

All admin endpoints require `Authorization: Bearer <admin_token>` with `role: "admin"`.

### GET `/api/admin/users`

List all users.

**Response (200):**
```json
{
  "users": [
    {
      "id": 1,
      "firstname": "John",
      "lastname": "Doe",
      "email": "john@example.com",
      "phone": "1234567890",
      "role": "citizen",
      "created_at": "2025-01-15T10:30:00"
    }
  ]
}
```

---

### DELETE `/api/admin/users/<id>`

Delete a user.

**Response (200):**
```json
{
  "message": "User deleted successfully"
}
```

**Errors:**
- `404` — User not found

---

### GET `/api/admin/issues`

List all issues (admin view with full details).

**Response (200):**
```json
{
  "issues": [
    {
      "id": 1,
      "title": "...",
      "status": "pending",
      "citizen": {
        "id": 1,
        "firstname": "John",
        "lastname": "Doe"
      },
      "department": null,
      ...
    }
  ]
}
```

---

### PUT `/api/admin/issues/<id>/status`

Update issue status.

**Request Body:**
```json
{
  "status": "in_progress"
}
```

**Valid statuses:** `pending`, `in_progress`, `resolved`, `rejected`, `verified`

**Response (200):**
```json
{
  "message": "Status updated successfully",
  "issue": { ... }
}
```

---

### GET `/api/admin/departments`

List all departments.

**Response (200):**
```json
{
  "departments": [
    {
      "id": 1,
      "name": "Public Works",
      "description": "Roads and infrastructure",
      "contact_email": "works@city.gov",
      "contact_phone": "555-0100"
    }
  ]
}
```

---

### POST `/api/admin/departments`

Create a new department.

**Request Body:**
```json
{
  "name": "Public Works",
  "description": "Roads and infrastructure maintenance",
  "contact_email": "works@city.gov",
  "contact_phone": "555-0100"
}
```

**Response (201):**
```json
{
  "message": "Department created successfully",
  "department": { ... }
}
```

---

### PUT `/api/admin/issues/<id>/department`

Assign a department to an issue.

**Request Body:**
```json
{
  "department_id": 1
}
```

**Response (200):**
```json
{
  "message": "Department assigned successfully",
  "issue": { ... }
}
```

---

### POST `/api/admin/issues/<id>/updates`

Post an update on an issue.

**Request Body (multipart/form-data):**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | Yes | Update title |
| `body` | string | No | Update body text |
| `progress` | int | No | Progress percentage (0-100) |
| `images` | file[] | No | Images for this update |

**Response (201):**
```json
{
  "message": "Update posted successfully",
  "update": {
    "id": 1,
    "title": "Investigation Started",
    "body": "Team dispatched...",
    "progress": 25,
    "image_urls": [],
    "created_at": "2025-01-16T09:00:00"
  }
}
```

---

## Health Check

### GET `/ping`

No auth required.

**Response (200):**
```json
{
  "status": "pong"
}
```

---

## Error Response Format

All errors follow this format:

```json
{
  "message": "Error description"
}
```

Common HTTP status codes:
| Code | Meaning |
|------|---------|
| `400` | Bad Request — Missing/invalid fields |
| `401` | Unauthorized — Invalid or missing token |
| `403` | Forbidden — Insufficient permissions |
| `404` | Not Found — Resource doesn't exist |
| `409` | Conflict — Duplicate resource |
| `413` | Payload Too Large — File exceeds limit |
| `500` | Internal Server Error |
