import logging
from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from src.notifications.exceptions import NotificationException
from src.database import get_db_session
from src.notifications import _create_notification, _update_notification, _get_notifications, \
    _delete_notification

from src.notifications.schemes import NotificationRequestModel, UpdateNotificationRequestModel, \
    GetNotificationsRequestModel, DeleteNotificationRequestModel


notifications_router = APIRouter(prefix=f"/notifications")
logger = logging.getLogger(__name__)


@notifications_router.post("/")
async def create_notification(notification: NotificationRequestModel, db: AsyncSession = Depends(get_db_session)):
    try:
        await _create_notification(notification, db)
        return JSONResponse(content={}, status_code=status.HTTP_201_CREATED)
    except NotificationException as exception:
        return JSONResponse(content={"message": exception.detail}, status_code=exception.status_code)
    except Exception as exception:
        logger.exception(f"Server Exception: {exception}")
        return JSONResponse(content={}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@notifications_router.put("/")
async def update_notification(notification: UpdateNotificationRequestModel, db: AsyncSession = Depends(get_db_session)):
    try:
        await _update_notification(notification, db)
        return JSONResponse(content={}, status_code=status.HTTP_200_OK)
    except NotificationException as exception:
        return JSONResponse(content={"message": exception.detail}, status_code=exception.status_code)
    except Exception as exception:
        logger.exception(f"Server Exception: {exception}")
        return JSONResponse(content={}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@notifications_router.post("/list")
async def get_notifications(notification: GetNotificationsRequestModel, db: AsyncSession = Depends(get_db_session)):
    try:
        response = await _get_notifications(notification, db)
        return JSONResponse(content={"data": response}, status_code=status.HTTP_200_OK)
    except NotificationException as exception:
        return JSONResponse(content={"message": exception.detail}, status_code=exception.status_code)
    except Exception as exception:
        logger.exception(f"Server Exception: {exception}")
        return JSONResponse(content={}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@notifications_router.delete("/")
async def delete_notification(notification: DeleteNotificationRequestModel, db: AsyncSession = Depends(get_db_session)):
    try:
        await _delete_notification(notification, db)
        return JSONResponse(content={}, status_code=status.HTTP_200_OK)
    except NotificationException as exception:
        return JSONResponse(content={"message": exception.detail}, status_code=exception.status_code)
    except Exception as exception:
        logger.exception(f"Server Exception: {exception}")
        return JSONResponse(content={}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)