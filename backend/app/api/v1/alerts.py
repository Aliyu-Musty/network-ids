from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.models.alert import AttackAlert
from app.schemas.alert import AttackAlertResponse, AttackAlertCreate

router = APIRouter()

@router.get("/", response_model=List[AttackAlertResponse])
async def get_alerts(
    skip: int = 0,
    limit: int = 50,
    severity: Optional[str] = None,
    attack_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(AttackAlert).order_by(AttackAlert.timestamp.desc())

    if severity:
        query = query.where(AttackAlert.severity == severity.upper())
    if attack_type:
        query = query.where(AttackAlert.attack_type == attack_type)

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    alerts = result.scalars().all()
    return alerts

@router.post("/", response_model=AttackAlertResponse)
async def create_alert(
    alert_in: AttackAlertCreate,
    db: AsyncSession = Depends(get_db)
):
    alert = AttackAlert(**alert_in.dict())
    db.add(alert)
    await db.commit()
    await db.refresh(alert)
    return alert
