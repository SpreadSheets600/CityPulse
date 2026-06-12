# CityPulse Roadmap

## Current Status

CityPulse is a **functional MVP** with core issue reporting, management, and admin capabilities. The foundation is solid — JWT auth, role-based access, media handling, geolocation, and a clean admin workflow.

---

## Phase 1: Stabilization & Polish (1-2 weeks)

Priority: Fix known issues and harden the existing system.

| Task | Priority | Effort | Details |
|------|----------|--------|---------|
| Move S3 credentials to env vars | High | Low | Security fix — currently hardcoded |
| Add CORS restriction for production | High | Low | Only allow production domain |
| Fix VerificationStatus model naming | High | Low | Enum shadows class name |
| Remove dead `users.py` route file | Low | Low | Unused Blueprint file |
| Add pagination to issue lists | High | Medium | Prevent loading all records at once |
| Fix duplicate CORS initialization | Low | Low | `CORS()` called twice in `app.py` |
| Add error boundary to frontend | Medium | Low | Catch and display component errors |
| Add loading skeletons | Medium | Low | Better UX during data fetching |

---

## Phase 2: Core Enhancements (2-4 weeks)

Priority: Add missing features that users expect.

| Feature | Priority | Effort | Description |
|---------|----------|--------|-------------|
| **User Profile Edit** | High | Low | Allow users to update name, phone, address, profile picture |
| **Password Reset** | High | Medium | Email-based password reset flow |
| **Email Notifications** | High | Medium | Notify citizens when issue status changes |
| **Search & Filter** | High | Medium | Full-text search + filter by type, status, date range |
| **Issue Upvoting** | Medium | Medium | Citizens can upvote issues to show priority |
| **Comments System** | Medium | Medium | Threaded comments on issues |
| **Audit Log** | Medium | Medium | Track all admin actions for accountability |
| **Rate Limiting** | High | Low | Prevent API abuse with Flask-Limiter |

---

## Phase 3: Advanced Features (1-2 months)

Priority: Differentiation and advanced capabilities.

| Feature | Priority | Effort | Description |
|---------|----------|--------|-------------|
| **Analytics Dashboard** | Medium | High | Charts, trends, resolution time metrics |
| **Export Reports** | Medium | Medium | CSV/PDF export of issues data |
| **Geofencing** | Medium | Medium | Auto-assign issues to departments by location |
| **SLA Tracking** | Medium | Medium | Track resolution time vs SLA targets |
| **Multi-Language Support** | Low | High | i18n for different languages |
| **Image Annotations** | Low | High | Draw/mark on images to highlight issues |
| **SMS Notifications** | Medium | Medium | Twilio/AWS SNS for SMS updates |
| **Push Notifications** | Medium | High | Browser push notifications |

---

## Phase 4: Platform Expansion (2-3 months)

Priority: Scale and modernize.

| Feature | Priority | Effort | Description |
|---------|----------|--------|-------------|
| **Docker Setup** | High | Medium | Docker Compose for easy deployment |
| **CI/CD Pipeline** | High | Medium | GitHub Actions for automated testing/deployment |
| **Unit Tests** | High | Medium | pytest for backend, Vitest for frontend |
| **Integration Tests** | Medium | High | API endpoint testing |
| **E2E Tests** | Medium | High | Playwright/Cypress for full user flows |
| **API Versioning** | Medium | Medium | v1/v2 API versioning |
| **GraphQL API** | Low | High | Alternative to REST for complex queries |
| **SSO Integration** | Medium | Medium | OAuth2 login (Google, GitHub) |
| **Webhook System** | Low | Medium | Notify external systems on events |

---

## Phase 5: Intelligence & Mobile (3-6 months)

Priority: AI features and native mobile.

| Feature | Priority | Effort | Description |
|---------|----------|--------|-------------|
| **AI Issue Classification** | Medium | High | Auto-categorize issues from images/text |
| **Duplicate Detection** | Medium | High | Identify similar/reported issues |
| **Priority Scoring** | Low | High | AI-based urgency ranking |
| **Mobile App** | Medium | Very High | React Native / Flutter native app |
| **Offline Support** | Low | High | Cache and sync when online |
| **Live Chat** | Low | High | Real-time admin-citizen communication |
| **Chatbot** | Low | High | AI chatbot for issue reporting guidance |

---

## Technical Debt

| Issue | Severity | Location | Fix |
|-------|----------|----------|-----|
| S3 credentials hardcoded | High | `config.py:20-21` | Move to env vars |
| CORS allows all origins | High | `app.py:40-41` | Restrict in production |
| No tests | High | Project-wide | Add pytest + Vitest |
| No pagination | Medium | All issue endpoints | Add limit/offset params |
| Duplicate form logic | Medium | `Issue-Form.vue` + `Issue-Create.vue` | Extract shared logic |
| GeoAlchemy2 unused | Low | `issue.py:3` | Remove or implement |
| `users.py` dead code | Low | `routes/users.py` | Delete file |
| No database migrations dir | Low | `backend/` | Run `flask db init` |

---

## Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Issue report time | ~2 min | < 1 min |
| Issue resolution time | Unknown | < 7 days |
| User registration | Manual | Email verification |
| Admin response rate | Unknown | Dashboard metrics |
| API response time | Unknown | < 200ms p95 |
| Test coverage | 0% | > 80% |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to CityPulse.
