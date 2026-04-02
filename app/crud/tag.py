from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagUpdate


async def get_tag(db: AsyncSession, tag_id: int) -> Tag | None:
    result = await db.execute(select(Tag).where(Tag.id == tag_id, Tag.is_deleted == False))
    return result.scalar_one_or_none()


async def list_tags(db: AsyncSession, limit: int, offset: int) -> list[Tag]:
    result = await db.execute(
        select(Tag).where(Tag.is_deleted == False).offset(offset).limit(limit)
    )
    return list(result.scalars().all())


async def create_tag(db: AsyncSession, obj_in: TagCreate) -> Tag:
    db_obj = Tag(**obj_in.model_dump())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def update_tag(db: AsyncSession, db_obj: Tag, obj_in: TagUpdate) -> Tag:
    data = obj_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(db_obj, field, value)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def soft_delete_tag(db: AsyncSession, db_obj: Tag) -> Tag:
    db_obj.is_deleted = True
    await db.commit()
    await db.refresh(db_obj)
    return db_obj
