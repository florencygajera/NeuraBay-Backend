from pydantic import BaseModel, ConfigDict


class TestimonialBase(BaseModel):
    name: str
    role: str | None = None
    company: str | None = None
    content: str
    rating: int | None = None
    is_approved: bool = False


class TestimonialCreate(TestimonialBase):
    pass


class TestimonialUpdate(BaseModel):
    name: str | None = None
    role: str | None = None
    company: str | None = None
    content: str | None = None
    rating: int | None = None
    is_approved: bool | None = None


class TestimonialOut(TestimonialBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
