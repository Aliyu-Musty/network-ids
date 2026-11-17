from pydantic import BaseModel
from datetime import datetime

class TrafficLogBase(BaseModel):
    src_ip: str
    dst_ip: str
    protocol: str
    packet_length: int
    classification: str

class TrafficLogCreate(TrafficLogBase):
    pass

class TrafficLogResponse(TrafficLogBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class SystemStats(BaseModel):
    total_packets: int
    total_attacks: int
    critical_alerts: int
    active_threats: int
