from sqlalchemy.ext.asyncio import AsyncSession
from app.models.application import Application
from app.schemas.application import ApplicationCreate


async def create_application(db: AsyncSession, obj_in: ApplicationCreate) -> Application:
    db_obj = Application(**obj_in.model_dump())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj
