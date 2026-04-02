from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.blog import create_blog, update_blog, list_blogs, get_blog, soft_delete_blog
from app.schemas.blog import BlogCreate, BlogUpdate


async def create_blog_post(db: AsyncSession, obj_in: BlogCreate, author_id: int | None):
    return await create_blog(db, obj_in, author_id)


async def update_blog_post(db: AsyncSession, db_obj, obj_in: BlogUpdate):
    return await update_blog(db, db_obj, obj_in)


async def delete_blog_post(db: AsyncSession, db_obj):
    return await soft_delete_blog(db, db_obj)


async def list_blog_posts(db: AsyncSession, limit: int, offset: int, search: str | None, category_id: int | None, tag_id: int | None):
    return await list_blogs(db, limit, offset, search, category_id, tag_id)


async def get_blog_post(db: AsyncSession, blog_id: int):
    return await get_blog(db, blog_id)
