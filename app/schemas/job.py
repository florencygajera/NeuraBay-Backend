from datetime import datetime
from pydantic import BaseModel, ConfigDict


class JobBase(BaseModel):
    title: str
    location: str | None = None
    job_type: str | None = None
    description: str
    is_active: bool = True


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    title: str | None = None
    location: str | None = None
    job_type: str | None = None
    description: str | None = None
    is_active: bool | None = None


class JobOut(JobBase):
    id: int
    posted_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
