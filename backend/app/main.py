import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api import auth, users, tickets, attachments, notifications
from app.api import settings as settings_router

app = FastAPI(
    title=settings.APP_NAME,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

# CORS: allow localhost for dev + any production origins from env
allowed_origins = ["http://localhost:5173", "http://localhost:3000"]
extra_origins = os.environ.get("ALLOWED_ORIGINS", "")
if extra_origins:
    allowed_origins.extend([o.strip() for o in extra_origins.split(",") if o.strip()])

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tickets.router)
app.include_router(attachments.router)
app.include_router(notifications.router)
app.include_router(settings_router.router)


@app.get("/api/health")
def health():
    return {"status": "ok", "service": settings.APP_NAME}
