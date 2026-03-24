# Helpdesk System — Full Build Prompt

Use this prompt with any AI coding assistant to recreate the entire helpdesk application from scratch.

---

## Tech Stack
- Backend: Python 3.11 + FastAPI + SQLAlchemy + Alembic (PostgreSQL 16)
- Frontend: React 18 + TypeScript + TailwindCSS + Vite
- Task Queue: Celery + Redis
- Auth: JWT (python-jose) + bcrypt password hashing
- Icons: Lucide React
- HTTP Client: Axios
- Containerization: Docker + Docker Compose (all services)

---

## Database Models

1. **User** — id, name, email, hashed_password, role (admin/manager/agent/client), team, is_active, timestamps
2. **Ticket** — id, subject, description, category (Bug/Feature/Access/Infra/General/Urgent), priority (Low/Medium/High/Critical), status (open/in_progress/resolved/closed), project, reporter_id, reporter_email, sla_deadline, timestamps
3. **TicketComment** — id, ticket_id, author_id, author_email, body, source (web/email), timestamps
4. **TicketAssignment** — id, ticket_id, agent_id, assigned_by, timestamps
5. **Attachment** — id, ticket_id, comment_id (nullable), filename, original_filename, content_type, size_bytes, storage_path, uploaded_at
6. **Notification** — id, user_id, ticket_id, message, is_read, timestamps
7. **EmailLog** — id, ticket_id, direction, subject, from_addr, to_addr, message_id, in_reply_to, timestamps
8. **SLAPolicy** — id, priority, response_hours, resolution_hours, is_active
9. **Setting** — id, key (unique), value, category, label, description, value_type (string/integer/boolean/password), timestamps

---

## Backend API Endpoints

### Auth
- POST `/api/auth/register`
- POST `/api/auth/login`

### Users
- GET `/api/users/me` — Current user profile
- GET `/api/users/` — List users, filterable by role (admin/manager only)
- GET `/api/users/{id}` — Get user by ID
- PUT `/api/users/{id}` — Update user name, role, team, is_active (admin only)

### Tickets
- GET `/api/tickets/` — List tickets, filtered/paginated, clients see own only
- POST `/api/tickets/` — Create ticket
- GET `/api/tickets/{id}` — Get ticket detail
- PUT `/api/tickets/{id}` — Update ticket (staff only)
- POST `/api/tickets/{id}/assign` — Assign agent to ticket
- GET `/api/tickets/{id}/comments` — List comments
- POST `/api/tickets/{id}/comments` — Add comment
- GET `/api/tickets/{id}/attachments` — List attachments

### Attachments
- POST `/api/attachments/upload` — Multipart FormData with ticket_id + files; validates extensions and size limits
- GET `/api/attachments/{id}/download` — Auth via `?token=` query param for browser links

### Settings
- GET `/api/settings/` — List settings, filterable by category (admin/manager)
- PUT `/api/settings/` — Bulk update settings (admin only)

### Notifications
- GET `/api/notifications/` — List notifications
- PUT `/api/notifications/{id}/read` — Mark notification read
- PUT `/api/notifications/read-all` — Mark all read

---

## Email Integration (Celery Workers)

- IMAP polling to read incoming emails and create tickets
- Subject format validation: `[Category] Summary`
- Body format: Project, Priority, Description fields
- Auto-reply with format template when email doesn't match
- Email threading via In-Reply-To headers
- Attachment extraction from emails

---

## Frontend Pages

### 1. LoginPage
- Centered card with email/password fields
- Dark gradient background
- Default credentials hint at bottom

### 2. TicketListPage
- Card-style ticket list (not table rows)
- Status/priority/category filter dropdowns + search by project
- Color-coded status badges (blue=open, yellow=in_progress, green=resolved, gray=closed)
- Color-coded priority text
- Attachment count indicator with paperclip icon
- Click any ticket to open detail

### 3. CreateTicketPage
- Form: subject, category dropdown, priority dropdown, project text, description textarea
- Drag-and-drop file upload area below description
- File list with type-specific icons (image, document, spreadsheet, archive)
- Each file shows name, size, and remove (X) button
- Total file count and size counter
- Two-step submit: create ticket first, then upload attachments to the new ticket ID

### 4. TicketDetailPage
- Two-column layout
- **Left column**: ticket header (ID, subject, status badge), description, attachments section (with Preview link for images/PDFs and Download link), comments thread (author, timestamp, source badge), add comment form
- **Right sidebar**: Details panel (category, project, priority, reporter, created date, SLA deadline), Actions panel (status dropdown, assign-to-agent dropdown) — visible to staff only

### 5. AdminUsersPage
- User table with avatar initials circle, name, email, role badge (color-coded), team, status (Active/Disabled toggle), Edit button
- Role filter dropdown at top
- Add User button opens modal (name, email, password, role, team)
- Edit button opens modal (name, role, team, active toggle — email read-only)

### 6. AdminSettingsPage
- Grouped settings sections with icons (General, Email Configuration, Attachments, Auto-Reply)
- Type-aware inputs: text fields for strings, number fields for integers, toggle switches for booleans, password fields with show/hide for sensitive values
- Blue dot indicator next to changed settings
- Save Changes and Discard buttons appear when changes exist

---

## Layout & Navigation

- Fixed left sidebar (dark bg-gray-900):
  - Helpdesk logo with lifebuoy icon
  - Tickets link
  - New Ticket link
  - Admin section header (visible only to admin/manager)
  - Users link (admin/manager only)
  - Settings link (admin/manager only)
  - User avatar (initials circle) + name + role at bottom
  - Logout button
- Main content area: gray-50 background, max-width container, padding

---

## Seed Data Script

Create a seed script (`python -m app.seed`) that populates:

### Users (8 total)
| Role | Name | Email | Password | Team |
|------|------|-------|----------|------|
| Admin | Admin | admin@company.com | admin123 | Engineering |
| Manager | Sarah Manager | manager@company.com | manager123 | Support |
| Agent | Support Agent | agent@company.com | agent123 | Support |
| Agent | DevOps Agent | devops@company.com | agent123 | Infrastructure |
| Agent | QA Agent | qa@company.com | agent123 | Quality |
| Client | John Client | john@client.com | client123 | — |
| Client | Jane Client | jane@client.com | client123 | — |
| Client | Bob Client | bob@client.com | client123 | — |

### Also seed:
- Default SLA policies for each priority level
- System settings: app name, session timeout, IMAP/SMTP config (host, port, username, password, SSL, poll interval), attachment limits (max size, max total, allowed extensions), auto-reply cooldown
- 12 sample tickets across different categories, priorities, statuses, and reporters
- 10 comments across various tickets from different authors
- 6 agent assignments
- Clean deletion of existing data before re-seeding (delete in FK order: assignments, comments, notifications, attachments, email logs, tickets, then users)

---

## Config & Environment

### .env file
```
DATABASE_URL=postgresql://helpdesk:helpdesk@db:5432/helpdesk
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your-secret-key
IMAP_HOST=imap.example.com
IMAP_PORT=993
IMAP_USER=support@company.com
IMAP_PASS=password
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=support@company.com
SMTP_PASS=password
```

### Attachment config (in app config)
```
UPLOAD_DIR=uploads
MAX_ATTACHMENT_SIZE_MB=10
MAX_TOTAL_ATTACHMENT_SIZE_MB=25
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif,pdf,doc,docx,xls,xlsx,csv,txt,zip,tar.gz,log
```

---

## Docker Compose Services

1. **db** — PostgreSQL 16, volume for persistence
2. **redis** — Redis 7
3. **backend** — FastAPI with uvicorn, auto-reload, volume mount for code, depends on db + redis
4. **celery-worker** — Celery worker process
5. **celery-beat** — Celery beat scheduler for email polling
6. **frontend** — Vite dev server with proxy forwarding /api/* to backend container

---

## Key Implementation Details

- JWT token stores user ID as string in `sub` claim; decode converts back to int
- Frontend stores token in `localStorage`; Axios interceptor adds `Authorization: Bearer <token>` header
- Attachment downloads use `?token=` query param since `<a href>` tags cannot send Authorization headers
- Vite proxy forwards `/api/*` requests to the backend container hostname
- Frontend uses React Router for client-side routing
- All forms have loading states and error display
- File upload UI shows type-specific icons (Image, FileText, FileSpreadsheet, FileArchive from Lucide)
- Role-based access control on both backend (dependency injection) and frontend (conditional rendering)
- Settings use a generic key-value model with metadata (category, label, description, value_type) for dynamic UI rendering
