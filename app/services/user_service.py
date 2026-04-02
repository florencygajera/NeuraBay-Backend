from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import list_users, get_user, update_user, soft_delete_user
from app.schemas.user import UserUpdate


async def list_user_items(db: AsyncSession, limit: int, offset: int):
    return await list_users(db, limit, offset)


async def get_user_item(db: AsyncSession, user_id: int):
    return await get_user(db, user_id)


async def update_user_item(db: AsyncSession, db_obj, obj_in: UserUpdate):
    return await update_user(db, db_obj, obj_in)


async def delete_user_item(db: AsyncSession, db_obj):
    return await soft_delete_user(db, db_obj)
