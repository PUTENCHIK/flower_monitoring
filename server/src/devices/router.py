from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
import logging
from src.database import get_db_session

from src.devices import TokenSecuredRequestModel, UpdateDataRequestModel, _register_device, \
    _update_data, TokenRequestModel, _get_data, UpdateConfigRequestModel, _update_config, _get_config, \
        _check_password

from src.devices.exceptions import DeviceException

devices_router = APIRouter(prefix=f"/devices")
logger = logging.getLogger(__name__)


@devices_router.post("/register")
async def register_device(device: TokenSecuredRequestModel, db: AsyncSession = Depends(get_db_session)):
    try:
        await _register_device(device, db)
        return JSONResponse(content={}, status_code=status.HTTP_201_CREATED)
    except DeviceException as exception:
        return JSONResponse(content={"message": exception.detail}, status_code=exception.status_code)
    except Exception as exception:
        logger.exception(f"Server Exception: {exception}")
        return JSONResponse(content={}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@devices_router.patch("/data")
async def update_data(device: UpdateDataRequestModel, db: AsyncSession = Depends(get_db_session)):
    try:
        await _update_data(device, db)

        return JSONResponse(content={}, status_code=status.HTTP_200_OK)
    except DeviceException as exception:
        return JSONResponse(content={"message": exception.detail}, status_code=exception.status_code)
    except Exception as exception:
        logger.exception(f"Server Exception: {exception}")
        return JSONResponse(content={}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@devices_router.post("/data")
async def get_data(device: TokenRequestModel, db: AsyncSession = Depends(get_db_session)):
    try:
        response = await _get_data(device, db)

        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    except DeviceException as exception:
        if exception.status_code == status.HTTP_204_NO_CONTENT:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        return JSONResponse(content={"message": exception.detail}, status_code=exception.status_code)
    except Exception as exception:
        logger.exception(f"Server Exception: {exception}")
        return JSONResponse(content={}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@devices_router.put("/config")
async def update_config(device: UpdateConfigRequestModel, db: AsyncSession = Depends(get_db_session)):
    try:
        await _update_config(device, db)

        return JSONResponse(content={}, status_code=status.HTTP_200_OK)
    except DeviceException as exception:
        return JSONResponse(content={"message": exception.detail}, status_code=exception.status_code)
    except Exception as exception:
        logger.exception(f"Server Exception: {exception}")
        return JSONResponse(content={}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@devices_router.post("/config")
async def get_config(device: TokenRequestModel, db: AsyncSession = Depends(get_db_session)):
    try:
        response = await _get_config(device, db)

        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    except DeviceException as exception:
        return JSONResponse(content={"message": exception.detail}, status_code=exception.status_code)
    except Exception as exception:
        logger.exception(f"Server Exception: {exception}")
        return JSONResponse(content={}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@devices_router.post("/password")
async def check_password(device: TokenSecuredRequestModel, db: AsyncSession = Depends(get_db_session)):
    try:
        await _check_password(device, db)

        return JSONResponse(content={}, status_code=status.HTTP_200_OK)
    except DeviceException as exception:
        return JSONResponse(content={"message": exception.detail}, status_code=exception.status_code)
    except Exception as exception:
        logger.exception(f"Server Exception: {exception}")
        return JSONResponse(content={}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)