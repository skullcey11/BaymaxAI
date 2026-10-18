# backend/api/reminder.py
import sys, os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime

# Ensure project root is on PYTHONPATH
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from backend.tools.reminder import add_reminder, list_upcoming

router = APIRouter()

class ReminderRequest(BaseModel):
    message: str
    remind_at: datetime  # ISO‑8601 datetime string

class ReminderResponse(BaseModel):
    reminder_id: int

@router.post("/reminder", response_model=ReminderResponse)
async def create_reminder(req: ReminderRequest):
    try:
        rid = add_reminder(req.message, req.remind_at)
        return ReminderResponse(reminder_id=rid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class UpcomingResponse(BaseModel):
    reminders: list

@router.get("/reminder/upcoming", response_model=UpcomingResponse)
async def get_upcoming(limit: int = 10):
    try:
        upcoming = list_upcoming(limit)
        return UpcomingResponse(reminders=upcoming)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
