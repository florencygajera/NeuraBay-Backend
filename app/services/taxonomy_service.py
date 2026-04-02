from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.category import create_category, update_category, list_categories, get_category, soft_delete_category
from app.crud.tag import create_tag, update_tag, list_tags, get_tag, soft_delete_tag
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.schemas.tag import TagCreate, TagUpdate


async def create_category_item(db: AsyncSession, obj_in: CategoryCreate):
    return await create_category(db, obj_in)


async def update_category_item(db: AsyncSession, db_obj, obj_in: CategoryUpdate):
    return await update_category(db, db_obj, obj_in)


async def list_category_items(db: AsyncSession, limit: int, offset: int):
    return await list_categories(db, limit, offset)


async def get_category_item(db: AsyncSession, category_id: int):
    return await get_category(db, category_id)


async def delete_category_item(db: AsyncSession, db_obj):
    return await soft_delete_category(db, db_obj)


async def create_tag_item(db: AsyncSession, obj_in: TagCreate):
    return await create_tag(db, obj_in)


async def update_tag_item(db: AsyncSession, db_obj, obj_in: TagUpdate):
    return await update_tag(db, db_obj, obj_in)


async def list_tag_items(db: AsyncSession, limit: int, offset: int):
    return await list_tags(db, limit, offset)


async def get_tag_item(db: AsyncSession, tag_id: int):
    return await get_tag(db, tag_id)


async def delete_tag_item(db: AsyncSession, db_obj):
    return await soft_delete_tag(db, db_obj)
