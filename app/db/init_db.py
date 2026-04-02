from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_password_hash
from app.models.user import User


async def init_db(session: AsyncSession) -> None:
    admin = await session.get(User, 1)
    if admin:
        return
    admin = User(
        email="admin@neurabay.com",
        full_name="Admin",
        hashed_password=get_password_hash("ChangeMe123!"),
        role="admin",
        is_active=True,
    )
    session.add(admin)
    await session.commit()
