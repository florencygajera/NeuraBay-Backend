from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import get_user_by_email, create_user
from app.schemas.user import UserCreate


async def register_user(db: AsyncSession, obj_in: UserCreate):
    existing = await get_user_by_email(db, obj_in.email)
    if existing:
        raise ValueError("Email already registered")
    return await create_user(db, obj_in)
