from pydantic import BaseModel
from datetime import time


class NotificationRequestModel(BaseModel):
    deviceToken: str
    password: str
    message: str
    days: int
    time: time
    enabled: bool


class UpdateNotificationRequestModel(NotificationRequestModel):
    notification_id: int


class GetNotificationsRequestModel(BaseModel):
    deviceToken: str


class DeleteNotificationRequestModel(BaseModel):
    deviceToken: str
    password: str
    notification_id: int