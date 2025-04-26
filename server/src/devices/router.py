from fastapi import APIRouter, Depends

devices_router = APIRouter(prefix=f"/devices")

# @classes_router.post("/add")
# async def add_class(class_: TrackableClassAddOrEdit, db: AsyncSession = Depends(get_db_session)):
#     new_class = await _add_class(class_, db)
#     return new_class


