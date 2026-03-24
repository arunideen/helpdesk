# Deploying Helpdesk to Railway

This guide walks you through deploying the helpdesk app to [Railway.app](https://railway.app) for a live demo.

---

## Prerequisites

- A [Railway account](https://railway.app) (sign up with GitHub)
- Your helpdesk repo pushed to GitHub: `https://github.com/arunideen/helpdesk.git`

---

## Step-by-Step Deployment

### 1. Create a New Project

1. Log in to [Railway Dashboard](https://railway.app/dashboard)
2. Click **New Project**
3. Select **Deploy from GitHub repo**
4. Connect your GitHub account if not already connected
5. Select the `arunideen/helpdesk` repository

### 2. Add PostgreSQL Database

1. In your project, click **New** → **Database** → **Add PostgreSQL**
2. Railway creates a PostgreSQL instance automatically
3. Note: Railway sets `DATABASE_URL` as a service variable — you'll reference this later

### 3. Add Redis

1. Click **New** → **Database** → **Add Redis**
2. Railway creates a Redis instance automatically
3. Note: Railway sets `REDIS_URL` as a service variable

### 4. Deploy the Backend Service

1. Click **New** → **GitHub Repo** → Select `arunideen/helpdesk`
2. Railway will ask which directory — set **Root Directory** to `backend`
3. Go to the service **Settings** tab:
   - **Service Name**: `backend`
   - **Root Directory**: `backend`
   - **Builder**: Dockerfile
4. Go to the **Variables** tab and add:

| Variable | Value |
|----------|-------|
| `DATABASE_URL` | `${{Postgres.DATABASE_URL}}` (click "Add Reference") |
| `REDIS_URL` | `${{Redis.REDIS_URL}}` (click "Add Reference") |
| `SECRET_KEY` | Generate a random string (e.g., `openssl rand -hex 32`) |
| `ALLOWED_ORIGINS` | Will be set after frontend deploys (the frontend URL) |
| `PORT` | `8000` |

5. Go to **Settings** → **Networking** → **Generate Domain** to get a public URL
6. Note the backend URL (e.g., `https://backend-production-xxxx.up.railway.app`)

### 5. Deploy the Frontend Service

1. Click **New** → **GitHub Repo** → Select `arunideen/helpdesk` again
2. Set **Root Directory** to `frontend`
3. Go to the service **Settings** tab:
   - **Service Name**: `frontend`
   - **Root Directory**: `frontend`
   - **Builder**: Dockerfile
   - **Dockerfile Path**: `Dockerfile.prod`
4. Go to the **Variables** tab and add:

| Variable | Value |
|----------|-------|
| `VITE_API_URL` | `https://backend-production-xxxx.up.railway.app/api` (your backend URL + `/api`) |
| `PORT` | `80` |

5. Go to **Settings** → **Networking** → **Generate Domain**
6. Note the frontend URL (e.g., `https://frontend-production-xxxx.up.railway.app`)

### 6. Update Backend CORS

1. Go back to your **backend** service → **Variables**
2. Set `ALLOWED_ORIGINS` to your frontend URL:
   ```
   https://frontend-production-xxxx.up.railway.app
   ```
3. The backend will redeploy automatically

### 7. Seed the Database

1. In the **backend** service, go to **Settings**
2. Temporarily change the **Start Command** to:
   ```
   python -m app.seed && uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
3. Or use the Railway CLI:
   ```bash
   railway run -s backend python -m app.seed
   ```

### 8. Access Your App

- **Frontend**: `https://frontend-production-xxxx.up.railway.app`
- **API Docs**: `https://backend-production-xxxx.up.railway.app/api/docs`
- **Login**: `admin@company.com` / `admin123`

---

## Custom Domain (Optional)

1. Go to your **frontend** service → **Settings** → **Networking**
2. Click **Custom Domain**
3. Enter your domain (e.g., `helpdesk.yourdomain.com`)
4. Add the CNAME record to your DNS provider as instructed
5. Update the backend `ALLOWED_ORIGINS` to include the custom domain

---

## Environment Variables Reference

### Backend Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `DATABASE_URL` | Yes | PostgreSQL connection string | `${{Postgres.DATABASE_URL}}` |
| `REDIS_URL` | Yes | Redis connection string | `${{Redis.REDIS_URL}}` |
| `SECRET_KEY` | Yes | JWT signing secret | Random 64-char hex string |
| `ALLOWED_ORIGINS` | Yes | Comma-separated allowed CORS origins | `https://frontend-xxx.up.railway.app` |
| `PORT` | Auto | Set by Railway automatically | `8000` |
| `IMAP_HOST` | No | Email polling (skip for demo) | `imap.gmail.com` |
| `SMTP_HOST` | No | Email sending (skip for demo) | `smtp.gmail.com` |

### Frontend Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `VITE_API_URL` | Yes | Backend API URL (must include `/api`) | `https://backend-xxx.up.railway.app/api` |

---

## Estimated Cost

Railway's free tier provides **$5/month** in credits. Typical usage for a demo:

| Service | Estimated Cost |
|---------|---------------|
| Backend (FastAPI) | ~$1-2/month |
| Frontend (nginx) | ~$0.50/month |
| PostgreSQL | ~$1/month |
| Redis | ~$0.50/month |
| **Total** | **~$3-4/month** (within free tier) |

---

## Troubleshooting

### Frontend shows blank page
- Check that `VITE_API_URL` is set correctly (must include `/api` suffix)
- Verify the Dockerfile is set to `Dockerfile.prod` in Railway settings

### API calls fail (CORS errors)
- Ensure `ALLOWED_ORIGINS` on the backend includes the exact frontend URL (with `https://`)
- Check the backend logs in Railway dashboard

### Database connection errors
- Verify `DATABASE_URL` references the Railway PostgreSQL service variable
- Check that the PostgreSQL service is running (green status)

### Seed data not loading
- Run the seed command via Railway CLI: `railway run -s backend python -m app.seed`
- Or set the start command to include seeding (see Step 7)

---

## Architecture on Railway

```
┌──────────────────────────────────────────────┐
│                Railway Project               │
│                                              │
│  ┌──────────┐   ┌──────────┐                │
│  │PostgreSQL│   │  Redis   │                │
│  │ Database │   │  Cache   │                │
│  └────┬─────┘   └────┬─────┘                │
│       │              │                       │
│  ┌────┴──────────────┴─────┐                │
│  │    Backend (FastAPI)     │                │
│  │  backend-xxx.railway.app│                │
│  └────────────┬────────────┘                │
│               │ CORS                        │
│  ┌────────────┴────────────┐                │
│  │  Frontend (React+nginx) │                │
│  │ frontend-xxx.railway.app│                │
│  └─────────────────────────┘                │
└──────────────────────────────────────────────┘
```
