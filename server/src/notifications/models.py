from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import BaseDBModel


class RegularNotification(BaseDBModel):
    __tablename__ = "regular_notifications"

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    message = Column(String(255), nullable=False)
    days = Column(Integer, nullable=False)
    time = Column(Time, nullable=False)
    isActive = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True)
    device = relationship("Device", back_populates="notifications")


class RegularNotificationChatIDs(BaseDBModel):
    __tablename__ = "regular_notification_chat_ids"

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    chat_id = Column(String(255), nullable=False)
    isActive = Column(Boolean, nullable=False)

    device = relationship("Device", back_populates="regular_chat_ids")


class СriticalNotificationChatIDs(BaseDBModel):
    __tablename__ = "critical_notification_chat_ids"

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    chat_id = Column(String(255), nullable=False)
    isActive = Column(Boolean, nullable=False)

    device = relationship("Device", back_populates="critical_chat_ids")