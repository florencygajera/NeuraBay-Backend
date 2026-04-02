from sqlalchemy import String, Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.base import IDMixin, TimestampMixin, SoftDeleteMixin


class Service(Base, IDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "services"

    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    created_by_user = relationship("User", back_populates="services")
