from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AttackAlertBase(BaseModel):
    attack_type: str
    severity: str
    confidence: float
    src_ip: str
    dst_ip: str
    src_port: Optional[int] = None
    dst_port: Optional[int] = None
    protocol: str
    packet_count: int = 1
    description: Optional[str] = None

class AttackAlertCreate(AttackAlertBase):
    pass

class AttackAlertResponse(AttackAlertBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
