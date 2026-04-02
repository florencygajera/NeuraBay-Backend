from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.testimonial import Testimonial
from app.schemas.testimonial import TestimonialCreate, TestimonialUpdate


async def get_testimonial(db: AsyncSession, testimonial_id: int) -> Testimonial | None:
    result = await db.execute(select(Testimonial).where(Testimonial.id == testimonial_id, Testimonial.is_deleted == False))
    return result.scalar_one_or_none()


async def list_testimonials(db: AsyncSession, limit: int, offset: int, approved_only: bool = False) -> list[Testimonial]:
    stmt = select(Testimonial).where(Testimonial.is_deleted == False)
    if approved_only:
        stmt = stmt.where(Testimonial.is_approved == True)
    result = await db.execute(stmt.offset(offset).limit(limit))
    return list(result.scalars().all())


async def create_testimonial(db: AsyncSession, obj_in: TestimonialCreate) -> Testimonial:
    db_obj = Testimonial(**obj_in.model_dump())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def update_testimonial(db: AsyncSession, db_obj: Testimonial, obj_in: TestimonialUpdate) -> Testimonial:
    data = obj_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(db_obj, field, value)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def soft_delete_testimonial(db: AsyncSession, db_obj: Testimonial) -> Testimonial:
    db_obj.is_deleted = True
    await db.commit()
    await db.refresh(db_obj)
    return db_obj
