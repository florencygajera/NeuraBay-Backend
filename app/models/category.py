from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.base import IDMixin, TimestampMixin, SoftDeleteMixin


class Category(Base, IDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)

    blogs = relationship("Blog", back_populates="category")
