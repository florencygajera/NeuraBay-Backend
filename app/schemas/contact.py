from pydantic import BaseModel, EmailStr, ConfigDict


class ContactBase(BaseModel):
    name: str
    email: EmailStr
    subject: str | None = None
    message: str


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    status: str | None = None


class ContactOut(ContactBase):
    id: int
    status: str

    model_config = ConfigDict(from_attributes=True)
