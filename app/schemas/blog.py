from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.schemas.tag import TagOut


class BlogBase(BaseModel):
    title: str
    slug: str
    summary: str | None = None
    content: str
    is_published: bool = False
    category_id: int | None = None
    tag_ids: list[int] = []


class BlogCreate(BlogBase):
    pass


class BlogUpdate(BaseModel):
    title: str | None = None
    slug: str | None = None
    summary: str | None = None
    content: str | None = None
    is_published: bool | None = None
    category_id: int | None = None
    tag_ids: list[int] | None = None


class BlogOut(BaseModel):
    id: int
    title: str
    slug: str
    summary: str | None = None
    content: str
    is_published: bool
    published_at: datetime | None = None
    category_id: int | None = None
    tag_ids: list[int] = []
    tags: list[TagOut] = []

    model_config = ConfigDict(from_attributes=True)
