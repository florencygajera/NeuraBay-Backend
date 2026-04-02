from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.service import create_service, update_service, list_services, get_service, soft_delete_service
from app.schemas.service import ServiceCreate, ServiceUpdate


async def create_service_item(db: AsyncSession, obj_in: ServiceCreate, created_by: int | None):
    return await create_service(db, obj_in, created_by)


async def update_service_item(db: AsyncSession, db_obj, obj_in: ServiceUpdate):
    return await update_service(db, db_obj, obj_in)


async def delete_service_item(db: AsyncSession, db_obj):
    return await soft_delete_service(db, db_obj)


async def list_service_items(db: AsyncSession, limit: int, offset: int):
    return await list_services(db, limit, offset)


async def get_service_item(db: AsyncSession, service_id: int):
    return await get_service(db, service_id)
