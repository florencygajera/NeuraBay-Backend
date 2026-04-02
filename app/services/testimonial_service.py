from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.testimonial import create_testimonial, list_testimonials, get_testimonial, update_testimonial, soft_delete_testimonial
from app.schemas.testimonial import TestimonialCreate, TestimonialUpdate


async def create_testimonial_item(db: AsyncSession, obj_in: TestimonialCreate):
    return await create_testimonial(db, obj_in)


async def list_testimonial_items(db: AsyncSession, limit: int, offset: int, approved_only: bool):
    return await list_testimonials(db, limit, offset, approved_only)


async def get_testimonial_item(db: AsyncSession, testimonial_id: int):
    return await get_testimonial(db, testimonial_id)


async def update_testimonial_item(db: AsyncSession, db_obj, obj_in: TestimonialUpdate):
    return await update_testimonial(db, db_obj, obj_in)


async def delete_testimonial_item(db: AsyncSession, db_obj):
    return await soft_delete_testimonial(db, db_obj)
