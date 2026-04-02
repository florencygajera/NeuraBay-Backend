from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.job import Job
from app.schemas.job import JobCreate, JobUpdate


async def get_job(db: AsyncSession, job_id: int) -> Job | None:
    result = await db.execute(select(Job).where(Job.id == job_id, Job.is_deleted == False))
    return result.scalar_one_or_none()


async def list_jobs(db: AsyncSession, limit: int, offset: int, active_only: bool = False) -> list[Job]:
    stmt = select(Job).where(Job.is_deleted == False)
    if active_only:
        stmt = stmt.where(Job.is_active == True)
    result = await db.execute(stmt.offset(offset).limit(limit))
    return list(result.scalars().all())


async def create_job(db: AsyncSession, obj_in: JobCreate) -> Job:
    data = obj_in.model_dump()
    db_obj = Job(**data, posted_at=datetime.now(timezone.utc))
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def update_job(db: AsyncSession, db_obj: Job, obj_in: JobUpdate) -> Job:
    data = obj_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(db_obj, field, value)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def soft_delete_job(db: AsyncSession, db_obj: Job) -> Job:
    db_obj.is_deleted = True
    await db.commit()
    await db.refresh(db_obj)
    return db_obj
