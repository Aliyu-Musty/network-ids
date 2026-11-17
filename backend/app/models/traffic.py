from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.core.database import Base

class TrafficLog(Base):
    __tablename__ = "traffic_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    src_ip = Column(String(45), nullable=False)
    dst_ip = Column(String(45), nullable=False)
    protocol = Column(String(10), nullable=False)
    packet_length = Column(Integer, nullable=False)
    classification = Column(String(50), default="BENIGN")
