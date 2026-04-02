from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


async def get_category(db: AsyncSession, category_id: int) -> Category | None:
    result = await db.execute(select(Category).where(Category.id == category_id, Category.is_deleted == False))
    return result.scalar_one_or_none()


async def list_categories(db: AsyncSession, limit: int, offset: int) -> list[Category]:
    result = await db.execute(
        select(Category).where(Category.is_deleted == False).offset(offset).limit(limit)
    )
    return list(result.scalars().all())


async def create_category(db: AsyncSession, obj_in: CategoryCreate) -> Category:
    db_obj = Category(**obj_in.model_dump())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def update_category(db: AsyncSession, db_obj: Category, obj_in: CategoryUpdate) -> Category:
    data = obj_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(db_obj, field, value)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def soft_delete_category(db: AsyncSession, db_obj: Category) -> Category:
    db_obj.is_deleted = True
    await db.commit()
    await db.refresh(db_obj)
    return db_obj
