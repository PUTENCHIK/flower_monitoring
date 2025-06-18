from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import BaseDBModel


class Device(BaseDBModel):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    deviceToken = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(255), nullable=True)
    last_activity = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True)
    ports = relationship("Port", back_populates="device")
    regular_chat_ids = relationship("RegularNotificationChatIDs", back_populates="device")
    critical_chat_ids = relationship("СriticalNotificationChatIDs", back_populates="device")
    notifications = relationship("RegularNotification", back_populates="device")


class Port(BaseDBModel):
    __tablename__ = "ports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    sensor_value = Column(Integer, nullable=True)
    port_number = Column(Integer, nullable=False)
    enabled = Column(Boolean, nullable=False)
    name = Column(String(255), nullable=False)
    low_level_boundary = Column(Integer, nullable=True)
    medium_level_boundary = Column(Integer, nullable=True)
    min_value = Column(Integer, nullable=False)
    max_value = Column(Integer, nullable=False)
    device = relationship("Device", back_populates="ports")