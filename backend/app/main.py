import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from .routers import users as users_router
from .routers import contents as contents_router
from fastapi.staticfiles import StaticFiles
from .db.session import engine, Base
from . import config

app = FastAPI(title="FDI System API")

# CORS (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB init (create tables if not exist)
Base.metadata.create_all(bind=engine)

# Static files and simple admin panel
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

app.include_router(users_router.router, prefix="/api/users", tags=["users"])
app.include_router(contents_router.router, prefix="/api/contents", tags=["contents"])

@app.get("/")
def root():
    return RedirectResponse(url="/docs")

@app.get("/admin")
def admin():
    return RedirectResponse(url="/static/admin.html")

@app.get("/api/health")
def health():
    return {"status": "ok"}

# Placeholder: bot webhook can be added later
# from .routers import bot_webhook
# app.include_router(bot_webhook.router, prefix="/api/bot", tags=["bot"])
