from pydantic import BaseModel, EmailStr, ConfigDict


class ApplicationBase(BaseModel):
    job_id: int
    name: str
    email: EmailStr
    resume_url: str | None = None
    cover_letter: str | None = None


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationOut(ApplicationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
