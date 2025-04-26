from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from server.src.database import BaseDBModel


class Device(BaseDBModel):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    deviceToken = Column(String, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String)
    last_activity = Column(DateTime)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    deleted_at = Column(DateTime)
    ports = relationship("Port", back_populates="device")


class Port(BaseDBModel):
    __tablename__ = "ports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    sensor_value = Column(Integer)
    port_number = Column(Integer, nullable=False)
    enabled = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)
    low_level_boundary = Column(Integer)
    medium_level_boundary = Column(Integer)
    device = relationship("Device", back_populates="ports")
