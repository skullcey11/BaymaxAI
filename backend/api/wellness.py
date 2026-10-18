# backend/api/wellness.py
import sys, os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

# Ensure project root is on PYTHONPATH
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from backend.tools.wellness import add_log, summary_last_days

router = APIRouter()

class WellnessLogRequest(BaseModel):
    water_intake: Optional[int] = None
    sleep_hours: Optional[float] = None
    exercise_minutes: Optional[int] = None
    mood: Optional[int] = None
    steps: Optional[int] = None
    weight_kg: Optional[float] = None

class WellnessLogResponse(BaseModel):
    entry_id: int

@router.post("/log", response_model=WellnessLogResponse)
async def log_wellness(req: WellnessLogRequest):
    try:
        entry_id = add_log(
            water_intake=req.water_intake,
            sleep_hours=req.sleep_hours,
            exercise_minutes=req.exercise_minutes,
            mood=req.mood,
            steps=req.steps,
            weight_kg=req.weight_kg,
        )
        return WellnessLogResponse(entry_id=entry_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class WellnessSummaryResponse(BaseModel):
    averages: dict

@router.get("/summary", response_model=WellnessSummaryResponse)
async def get_summary(days: int = 7):
    try:
        avgs = summary_last_days(days)
        return WellnessSummaryResponse(averages=avgs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
