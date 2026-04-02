from pydantic import BaseModel, ConfigDict


class TagBase(BaseModel):
    name: str
    slug: str


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None


class TagOut(TagBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
