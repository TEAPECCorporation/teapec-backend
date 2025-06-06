from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.core.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    log_id = Column(Integer, ForeignKey("logs.id"), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    severity = Column(String)
    description = Column(String)

    log = relationship("Log", back_populates="alerts")
