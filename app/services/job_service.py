from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.job import create_job, update_job, list_jobs, get_job, soft_delete_job
from app.crud.application import create_application
from app.schemas.job import JobCreate, JobUpdate
from app.schemas.application import ApplicationCreate


async def create_job_post(db: AsyncSession, obj_in: JobCreate):
    return await create_job(db, obj_in)


async def update_job_post(db: AsyncSession, db_obj, obj_in: JobUpdate):
    return await update_job(db, db_obj, obj_in)


async def delete_job_post(db: AsyncSession, db_obj):
    return await soft_delete_job(db, db_obj)


async def list_job_posts(db: AsyncSession, limit: int, offset: int, active_only: bool):
    return await list_jobs(db, limit, offset, active_only)


async def get_job_post(db: AsyncSession, job_id: int):
    return await get_job(db, job_id)


async def submit_application(db: AsyncSession, obj_in: ApplicationCreate):
    return await create_application(db, obj_in)
