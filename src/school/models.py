from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from src.database import Base

class DeviceType(enum.Enum):
    mobile = "mobile"
    desktop = "desktop"
    tablet = "tablet"

class Connectivity(enum.Enum):
    intermittent = "intermittent"
    online = "online"
    offline = "offline"

class School(Base):
    __tablename__ = "schools"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    region = Column(String, nullable=False)
    device_type = Column(Enum(DeviceType), nullable=True)
    connectivity = Column(Enum(Connectivity), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    teachers = relationship("Teacher", back_populates="school", cascade="all, delete-orphan")