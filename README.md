# Helpdesk System

An email-driven helpdesk ticketing system for software development companies. Supports both internal teams and external clients, with automatic email parsing, format validation, auto-reply, and attachment handling.

## Features

- **Email ingestion** — Polls IMAP mailbox, parses emails into tickets automatically
- **Format validation** — Validates subject `[Category]` tag and body fields (Project, Priority, Description)
- **Auto-reply** — Sends format template via SMTP when email doesn't match required format
- **Attachment support** — Extracts, validates (type/size), and stores email attachments
- **Web dashboard** — React-based UI for managing tickets, comments, assignments
- **Role-based access** — Admin, Manager, Agent, Client roles with JWT auth
- **Email threading** — Replies thread back to existing tickets via In-Reply-To headers
- **SLA tracking** — Automatic deadline calculation based on ticket priority

## Tech Stack

| Layer        | Technology              |
|-------------|------------------------|
| Backend     | Python 3.11 + FastAPI   |
| Frontend    | React 18 + TailwindCSS  |
| Database    | PostgreSQL 16           |
| Task Queue  | Celery + Redis          |
| Email       | IMAP (read) + SMTP (send) |
| Auth        | JWT (python-jose)       |

## Email Format

Emails sent to the helpdesk address must follow this format:

**Subject:**
```
[Category] Short summary
```
Categories: `Bug`, `Feature`, `Access`, `Infra`, `General`, `Urgent`

**Body:**
```
Project: <project-name>
Priority: Low | Medium | High | Critical
Description:
<detailed description>
```

**Attachments:** Optional. Max 10 MB per file, 25 MB total.
Supported: `png, jpg, gif, pdf, doc, docx, xls, xlsx, csv, txt, zip, tar.gz, log`

## Quick Start

### 1. Clone and configure

```bash
cp .env.example .env
# Edit .env with your IMAP/SMTP credentials
```

### 2. Start with Docker Compose

```bash
docker-compose up -d
```

This starts: PostgreSQL, Redis, FastAPI backend, Celery worker + beat, React frontend.

### 3. Initialize database and seed data

```bash
docker-compose exec backend python -m app.seed
```

Default users:
- **Admin:** `admin@company.com` / `admin123`
- **Agent:** `agent@company.com` / `agent123`

### 4. Access the app

- **Frontend:** http://localhost:5173
- **API Docs:** http://localhost:8000/api/docs
- **Health Check:** http://localhost:8000/api/health

## Local Development (without Docker)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start PostgreSQL and Redis locally, then:
uvicorn app.main:app --reload --port 8000
```

### Celery Worker

```bash
cd backend
celery -A app.workers.celery_app worker --loglevel=info
```

### Celery Beat (email polling scheduler)

```bash
cd backend
celery -A app.workers.celery_app beat --loglevel=info
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Running Tests

```bash
cd backend
pip install pytest
pytest tests/ -v
```

## API Endpoints

| Method | Endpoint                          | Description              |
|--------|-----------------------------------|--------------------------|
| POST   | `/api/auth/register`              | Register new user        |
| POST   | `/api/auth/login`                 | Login, get JWT token     |
| GET    | `/api/users/me`                   | Current user profile     |
| GET    | `/api/users/`                     | List users (admin/mgr)   |
| GET    | `/api/tickets/`                   | List tickets (filtered)  |
| POST   | `/api/tickets/`                   | Create ticket            |
| GET    | `/api/tickets/{id}`               | Get ticket detail        |
| PUT    | `/api/tickets/{id}`               | Update ticket            |
| POST   | `/api/tickets/{id}/assign`        | Assign agent             |
| GET    | `/api/tickets/{id}/comments`      | List comments            |
| POST   | `/api/tickets/{id}/comments`      | Add comment              |
| GET    | `/api/tickets/{id}/attachments`   | List attachments         |
| GET    | `/api/attachments/{id}/download`  | Download attachment      |
| GET    | `/api/notifications/`             | List notifications       |
| PUT    | `/api/notifications/{id}/read`    | Mark notification read   |
| PUT    | `/api/notifications/read-all`     | Mark all read            |

## Project Structure

```
helpdesk/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── config.py            # Settings from .env
│   │   ├── database.py          # SQLAlchemy engine & session
│   │   ├── seed.py              # DB seed script
│   │   ├── models/              # SQLAlchemy models
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── api/                 # Route handlers
│   │   ├── services/            # Business logic
│   │   ├── email/               # IMAP/SMTP + parser
│   │   ├── workers/             # Celery tasks
│   │   └── utils/               # Auth, storage helpers
│   ├── alembic/                 # DB migrations
│   ├── tests/                   # Unit tests
│   ├── uploads/                 # Attachment storage
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/Layout.tsx
│   │   ├── pages/               # Login, TicketList, TicketDetail, etc.
│   │   ├── hooks/useAuth.ts
│   │   └── services/api.ts      # Axios API client
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```
