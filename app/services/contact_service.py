from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.contact import create_contact, list_contacts, get_contact, update_contact
from app.schemas.contact import ContactCreate, ContactUpdate
from app.utils.email import send_email


async def create_contact_message(db: AsyncSession, obj_in: ContactCreate):
    contact = await create_contact(db, obj_in)
    await send_email(
        to_email=contact.email,
        subject="Thanks for contacting NeuraBay",
        body="We received your message and will get back to you shortly.",
    )
    return contact


async def list_contact_messages(db: AsyncSession, limit: int, offset: int):
    return await list_contacts(db, limit, offset)


async def get_contact_message(db: AsyncSession, contact_id: int):
    return await get_contact(db, contact_id)


async def update_contact_message(db: AsyncSession, db_obj, obj_in: ContactUpdate):
    return await update_contact(db, db_obj, obj_in)
