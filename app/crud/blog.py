from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.blog import Blog
from app.models.tag import Tag
from app.schemas.blog import BlogCreate, BlogUpdate


async def get_blog(db: AsyncSession, blog_id: int) -> Blog | None:
    result = await db.execute(
        select(Blog)
        .where(Blog.id == blog_id, Blog.is_deleted == False)
        .options(selectinload(Blog.tags))
    )
    return result.scalar_one_or_none()


async def list_blogs(
    db: AsyncSession,
    limit: int,
    offset: int,
    search: str | None = None,
    category_id: int | None = None,
    tag_id: int | None = None,
) -> list[Blog]:
    stmt = select(Blog).where(Blog.is_deleted == False).options(selectinload(Blog.tags))
    if search:
        stmt = stmt.where(Blog.title.ilike(f"%{search}%"))
    if category_id:
        stmt = stmt.where(Blog.category_id == category_id)
    if tag_id:
        stmt = stmt.join(Blog.tags).where(Tag.id == tag_id)
    stmt = stmt.offset(offset).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().unique().all())


async def create_blog(db: AsyncSession, obj_in: BlogCreate, author_id: int | None) -> Blog:
    db_obj = Blog(
        title=obj_in.title,
        slug=obj_in.slug,
        summary=obj_in.summary,
        content=obj_in.content,
        is_published=obj_in.is_published,
        published_at=datetime.now(timezone.utc) if obj_in.is_published else None,
        author_id=author_id,
        category_id=obj_in.category_id,
    )
    if obj_in.tag_ids:
        tags = (await db.execute(select(Tag).where(Tag.id.in_(obj_in.tag_ids)))).scalars().all()
        db_obj.tags = list(tags)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def update_blog(db: AsyncSession, db_obj: Blog, obj_in: BlogUpdate) -> Blog:
    data = obj_in.model_dump(exclude_unset=True)
    tag_ids = data.pop("tag_ids", None)
    for field, value in data.items():
        setattr(db_obj, field, value)
    if "is_published" in data and data["is_published"] and db_obj.published_at is None:
        db_obj.published_at = datetime.now(timezone.utc)
    if tag_ids is not None:
        tags = (await db.execute(select(Tag).where(Tag.id.in_(tag_ids)))).scalars().all()
        db_obj.tags = list(tags)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def soft_delete_blog(db: AsyncSession, db_obj: Blog) -> Blog:
    db_obj.is_deleted = True
    await db.commit()
    await db.refresh(db_obj)
    return db_obj
