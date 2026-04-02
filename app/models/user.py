from sqlalchemy import String, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.base import IDMixin, TimestampMixin, SoftDeleteMixin


class User(Base, IDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255))
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(Enum("admin", "user", name="user_roles"), default="user", index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    services = relationship("Service", back_populates="created_by_user")
    blogs = relationship("Blog", back_populates="author")
