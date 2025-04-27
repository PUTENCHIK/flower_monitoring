from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
import logging
from server.src.database import get_db_session
from server.src.devices import RegisterRequestModel, UpdateDataRequestModel, _register_device, \
    _update_data
from server.src.devices.exceptions import DeviceException

devices_router = APIRouter(prefix=f"/devices")
logger = logging.getLogger(__name__)

@devices_router.post("/register")
async def register_device(device: RegisterRequestModel, db: AsyncSession = Depends(get_db_session)):
    try:
        await _register_device(device, db)
    except DeviceException as exception:
        logger.exception(f"Client Error: {exception}")
        return JSONResponse(content={"message": exception.detail}, status_code=exception.status_code)
    except Exception as exception:
        logger.exception(f"Server Error: {exception}")
        return JSONResponse(content={}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JSONResponse(content={}, status_code=status.HTTP_201_CREATED)


@devices_router.patch("/data")
async def update_data(device: UpdateDataRequestModel, db: AsyncSession = Depends(get_db_session)):
    try:
        await _update_data(device, db)
    except DeviceException as exception:
        logger.exception(f"Client Error: {exception}")
        return JSONResponse(content={"message": exception.detail}, status_code=exception.status_code)
    except Exception as exception:
        logger.exception(f"Server Error: {exception}")
        return JSONResponse(content={}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JSONResponse(content={}, status_code=status.HTTP_200_OK)

