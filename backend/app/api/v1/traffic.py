from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from sqlalchemy.future import select

from app.core.database import get_db
from app.models.alert import AttackAlert
from app.models.traffic import TrafficLog
from app.schemas.traffic import SystemStats

router = APIRouter()

@router.get("/stats", response_model=SystemStats)
async def get_system_stats(db: AsyncSession = Depends(get_db)):
    # Total Attacks
    attacks_count = await db.scalar(select(func.count(AttackAlert.id))) or 0
    # Critical Alerts
    critical_count = await db.scalar(
        select(func.count(AttackAlert.id)).where(AttackAlert.severity == "CRITICAL")
    ) or 0
    # Total Packets
    traffic_count = await db.scalar(select(func.count(TrafficLog.id))) or 0

    return {
        "total_packets": traffic_count,
        "total_attacks": attacks_count,
        "critical_alerts": critical_count,
        "active_threats": max(critical_count // 2, 0)
    }
