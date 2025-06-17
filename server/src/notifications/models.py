from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import BaseDBModel


class Notification(BaseDBModel):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    message = Column(String(255), nullable=False)
    days = Column(Integer, nullable=False)
    time = Column(Time, nullable=False)
    enabled = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True)

    device = relationship("Device", back_populates="notifications")


class NotificationChatIDs(BaseDBModel):
    __tablename__ = "notification_chat_ids"

    id = Column(Integer, primary_key=True)
    notification_id = Column(Integer, ForeignKey("notifications.id"), nullable=True)
    chat_id = Column(String(255), nullable=True)