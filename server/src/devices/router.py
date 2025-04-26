from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from server.src.database import get_db_session
from server.src.devices import RegisterRequestModel, _register_device

devices_router = APIRouter(prefix=f"/devices")


@devices_router.post("/register")
async def register_device(device: RegisterRequestModel, db: AsyncSession = Depends(get_db_session)):
    await _register_device(device, db)
    return Response(status_code=status.HTTP_201_CREATED)


