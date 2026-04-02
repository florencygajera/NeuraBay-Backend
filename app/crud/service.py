from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.service import Service
from app.schemas.service import ServiceCreate, ServiceUpdate


async def get_service(db: AsyncSession, service_id: int) -> Service | None:
    result = await db.execute(select(Service).where(Service.id == service_id, Service.is_deleted == False))
    return result.scalar_one_or_none()


async def list_services(db: AsyncSession, limit: int, offset: int) -> list[Service]:
    result = await db.execute(
        select(Service).where(Service.is_deleted == False).offset(offset).limit(limit)
    )
    return list(result.scalars().all())


async def create_service(db: AsyncSession, obj_in: ServiceCreate, created_by: int | None) -> Service:
    db_obj = Service(**obj_in.model_dump(), created_by=created_by)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def update_service(db: AsyncSession, db_obj: Service, obj_in: ServiceUpdate) -> Service:
    data = obj_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(db_obj, field, value)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def soft_delete_service(db: AsyncSession, db_obj: Service) -> Service:
    db_obj.is_deleted = True
    await db.commit()
    await db.refresh(db_obj)
    return db_obj
