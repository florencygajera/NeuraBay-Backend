from pydantic import BaseModel, ConfigDict


class ServiceBase(BaseModel):
    title: str
    slug: str
    description: str | None = None
    is_active: bool = True


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    title: str | None = None
    slug: str | None = None
    description: str | None = None
    is_active: bool | None = None


class ServiceOut(ServiceBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
