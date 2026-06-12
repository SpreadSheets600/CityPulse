# CityPulse Features

## Current Features

### 1. Authentication System

| Feature | Status | Details |
|---------|--------|---------|
| User Registration | Implemented | Firstname, lastname, email, phone, address, password |
| Login (Email/Phone) | Implemented | Supports both email and phone number |
| JWT Authentication | Implemented | 7-day access tokens, header-based |
| Password Hashing | Implemented | bcrypt via passlib |
| Role-Based Access | Implemented | `citizen` and `admin` roles |
| Auto Profile Pictures | Implemented | DiceBear API avatar generation |

**Routes:**
- `POST /api/auth/register` — Register new user
- `POST /api/auth/login` — Login
- `POST /api/auth/logout` — Logout
- `POST /api/auth/refresh` — Refresh token
- `GET /api/auth/me` — Get current user

---

### 2. Issue Reporting (Citizens)

| Feature | Status | Details |
|---------|--------|---------|
| Multi-Field Form | Implemented | Title, description, type, location, media |
| 7 Issue Types | Implemented | Pothole, Street Light, Water Supply, Sewage, Garbage, Traffic, Other |
| Image Upload | Implemented | Multi-file, max 15MB, compressed to WEBP |
| Voice Notes | Implemented | Audio recording via MediaRecorder API |
| Video Notes | Implemented | Video recording with codec fallback |
| Browser Geolocation | Implemented | One-click location from device GPS |
| Interactive Map | Implemented | Click/drag on Leaflet map to set location |
| Address Search | Implemented | Nominatim autocomplete with suggestion list |
| Reverse Geocoding | Implemented | Convert coordinates to street address |

**Issue Types:**
1. 🕳️ Pothole
2. 💡 Street Light
3. 💧 Water Supply
4. 🚰 Sewage
5. 🗑️ Garbage
6. 🚦 Traffic
7. 📋 Other

---

### 3. Media Features

| Feature | Status | Details |
|---------|--------|---------|
| Photo Capture | Implemented | Webcam/device camera via getUserMedia |
| Audio Recording | Implemented | Microphone recording with visualization bars |
| Video Recording | Implemented | Camera recording with codec fallback |
| Image Compression | Implemented | Pillow-based, WEBP format, max 1.5MB |
| Image Lightbox | Implemented | Full-screen gallery with prev/next navigation |
| S3 Presigned URLs | Implemented | Secure temporary access to media (7-day expiry) |

**Media Storage:**
- Images compressed from original → WEBP → max 1.5MB
- Quality scales down proportionally to meet size limit
- All media stored in Synology C2 S3 bucket
- Access via presigned URLs (no direct S3 access)

---

### 4. Issue Management

| Feature | Status | Details |
|---------|--------|---------|
| View All Issues | Implemented | Authenticated users see all issues |
| View My Issues | Implemented | Filter to own reported issues |
| Issue Detail Page | Implemented | Full details, map, media, updates timeline |
| Add Images to Issue | Implemented | Upload additional images to existing issue |
| Status Tracking | Implemented | 5 states: pending, in_progress, resolved, rejected, verified |
| Department Assignment | Implemented | Assign issues to departments |
| Progress Updates | Implemented | Admin posts updates with title, body, progress % |
| Update Images | Implemented | Attach images to progress updates |

**Issue Statuses:**
```
pending → in_progress → resolved
    │          │            │
    │          │            └──→ verified
    │          │
    │          └──→ rejected
    │
    └──→ rejected
```

---

### 5. Public Features

| Feature | Status | Details |
|---------|--------|---------|
| Landing Page | Implemented | Hero section, feature cards, CTA |
| Public Reports Feed | Implemented | Live nearby reports (limited fields) |
| Interactive Map | Implemented | Leaflet map showing public issues |
| Status-Colored Markers | Implemented | Map markers colored by issue status |

---

### 6. Admin Dashboard

| Feature | Status | Details |
|---------|--------|---------|
| Admin Stats | Implemented | Total users, issues, status breakdown |
| Interactive Map | Implemented | All issues with status-colored markers |
| Issue List | Implemented | Filterable by status, type, date |
| User Management | Implemented | View all users, delete users |
| Issue Management | Implemented | Update status, assign department |
| Department Management | Implemented | Create departments, list all |
| Issue Updates | Implemented | Post updates with progress tracking |

**Admin Operations:**
- `GET /api/admin/users` — List all users
- `DELETE /api/admin/users/<id>` — Delete user
- `GET /api/admin/issues` — List all issues
- `PUT /api/admin/issues/<id>/status` — Update status
- `GET /api/admin/departments` — List departments
- `POST /api/admin/departments` — Create department
- `PUT /api/admin/issues/<id>/department` — Assign department
- `POST /api/admin/issues/<id>/updates` — Post update

---

### 7. UI/UX

| Feature | Status | Details |
|---------|--------|---------|
| Responsive Design | Implemented | Tailwind CSS responsive utilities |
| DaisyUI Components | Implemented | Modern UI component library |
| Dark Theme Ready | Implemented | DaisyUI theme support |
| Form Validation | Implemented | Client-side required fields |
| Loading States | Implemented | Visual feedback during API calls |
| Status Badges | Implemented | Color-coded issue status display |
| Navigation Guards | Implemented | Auth-based route protection |
| Auto-Redirect | Implemented | Admins → admin dashboard on login |

---

## Features We Can Implement

### High Priority

| Feature | Description | Effort |
|---------|-------------|--------|
| **Email Notifications** | Send email when issue status changes | Medium |
| **Push Notifications** | Browser push notifications for updates | Medium |
| **Pagination** | Paginate issue lists (currently returns all) | Low |
| **Search & Filter** | Full-text search + advanced filters on issues | Medium |
| **User Profile Edit** | Allow users to update profile info | Low |
| **Password Reset** | Email-based password reset flow | Medium |
| **Rate Limiting** | Prevent abuse on API endpoints | Low |
| **CORS Restriction** | Limit origins in production | Low |

### Medium Priority

| Feature | Description | Effort |
|---------|-------------|--------|
| **Issue Upvoting** | Citizens can upvote/like issues | Medium |
| **Comments System** | Allow citizens to comment on issues | Medium |
| **Issue Categories & Tags** | Sub-categories with tag system | Low |
| **Image Annotations** | Draw/mark on images to highlight issues | High |
| **Multi-Language Support** | i18n for different languages | High |
| **Analytics Dashboard** | Charts, graphs, trends for admin | Medium |
| **Export Reports** | CSV/PDF export of issues data | Medium |
| **SMS Notifications** | Twilio/SNS SMS for status updates | Medium |

### Low Priority (Future)

| Feature | Description | Effort |
|---------|-------------|--------|
| **Mobile App** | React Native / Flutter native app | Very High |
| **AI Issue Classification** | Auto-categorize issues from images/text | High |
| **Chatbot Support** | AI chatbot for issue reporting | High |
| **Geofencing** | Auto-assign issues to departments by location | Medium |
| **SLA Tracking** | Track resolution time vs SLA targets | Medium |
| **Citizen Verification** | Community verification of issues | Medium |
| **Live Chat** | Real-time admin-citizen communication | High |
| **Webhook Integration** | Notify external systems on events | Medium |
| **API Versioning** | v1/v2 API versioning | Medium |
| **GraphQL API** | Alternative to REST | High |
| **SSO Integration** | OAuth2 login (Google, GitHub) | Medium |
| **Audit Log** | Track all admin actions | Medium |

---

## Feature Comparison Matrix

| Capability | Current | Planned |
|-----------|---------|---------|
| Issue Reporting | ✅ Full | - |
| Media (Photo/Audio/Video) | ✅ Full | - |
| Geolocation | ✅ Full | - |
| Authentication | ✅ JWT | + OAuth2 |
| Role-Based Access | ✅ Basic | + Granular permissions |
| Admin Dashboard | ✅ Basic | + Analytics, Charts |
| Notifications | ❌ None | + Email, Push, SMS |
| Search | ❌ None | + Full-text, Filters |
| Pagination | ❌ None | + Infinite scroll |
| Comments | ❌ None | + Threaded comments |
| Upvoting | ❌ None | + Like/upvote system |
| Mobile | ⚠️ Responsive | + Native app |
| Testing | ❌ None | + Unit, Integration, E2E |
| CI/CD | ❌ None | + GitHub Actions |
| Docker | ❌ None | + Docker Compose |
