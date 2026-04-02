from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import require_admin
from app.db.session import get_db
from app.schemas.job import JobCreate, JobUpdate, JobOut
from app.schemas.application import ApplicationCreate, ApplicationOut
from app.services.job_service import create_job_post, update_job_post, list_job_posts, get_job_post, delete_job_post, submit_application
from app.utils.helpers import standard_response

router = APIRouter()


@router.get("/jobs", response_model=dict)
async def list_jobs(limit: int = 20, offset: int = 0, active_only: bool = False, db: AsyncSession = Depends(get_db)):
    jobs = await list_job_posts(db, limit, offset, active_only)
    return standard_response([JobOut.model_validate(j) for j in jobs], meta={"limit": limit, "offset": offset})


@router.post("/jobs", response_model=dict)
async def create_job(obj_in: JobCreate, db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    job = await create_job_post(db, obj_in)
    return standard_response(JobOut.model_validate(job))


@router.get("/jobs/{job_id}", response_model=dict)
async def get_job(job_id: int, db: AsyncSession = Depends(get_db)):
    job = await get_job_post(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return standard_response(JobOut.model_validate(job))


@router.put("/jobs/{job_id}", response_model=dict)
async def update_job(job_id: int, obj_in: JobUpdate, db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    job = await get_job_post(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    updated = await update_job_post(db, job, obj_in)
    return standard_response(JobOut.model_validate(updated))


@router.delete("/jobs/{job_id}", response_model=dict)
async def delete_job(job_id: int, db: AsyncSession = Depends(get_db), admin=Depends(require_admin)):
    job = await get_job_post(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    deleted = await delete_job_post(db, job)
    return standard_response({"id": deleted.id, "deleted": True})


@router.post("/jobs/apply", response_model=dict)
async def apply_job(obj_in: ApplicationCreate, db: AsyncSession = Depends(get_db)):
    application = await submit_application(db, obj_in)
    return standard_response(ApplicationOut.model_validate(application))
