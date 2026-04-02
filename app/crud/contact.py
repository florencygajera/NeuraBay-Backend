from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactUpdate


async def get_contact(db: AsyncSession, contact_id: int) -> Contact | None:
    result = await db.execute(select(Contact).where(Contact.id == contact_id, Contact.is_deleted == False))
    return result.scalar_one_or_none()


async def list_contacts(db: AsyncSession, limit: int, offset: int) -> list[Contact]:
    result = await db.execute(
        select(Contact).where(Contact.is_deleted == False).offset(offset).limit(limit)
    )
    return list(result.scalars().all())


async def create_contact(db: AsyncSession, obj_in: ContactCreate) -> Contact:
    db_obj = Contact(**obj_in.model_dump())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def update_contact(db: AsyncSession, db_obj: Contact, obj_in: ContactUpdate) -> Contact:
    data = obj_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(db_obj, field, value)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def soft_delete_contact(db: AsyncSession, db_obj: Contact) -> Contact:
    db_obj.is_deleted = True
    await db.commit()
    await db.refresh(db_obj)
    return db_obj
