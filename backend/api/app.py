# backend/api/app.py
import sys, os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure project root is on PYTHONPATH (backend __init__ already adds it)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from backend.api.chat import router as chat_router
from backend.api.reminder import router as reminder_router
from backend.api.wellness import router as wellness_router

app = FastAPI(title="Baymax AI Assistant API", version="0.1.0")

# Allow all origins for local development (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers under /api
app.include_router(chat_router, prefix="/api")
app.include_router(reminder_router, prefix="/api")
app.include_router(wellness_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Baymax AI Assistant API is running"}
