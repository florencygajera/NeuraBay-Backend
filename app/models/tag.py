from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.base import IDMixin, TimestampMixin, SoftDeleteMixin


class Tag(Base, IDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "tags"

    name: Mapped[str] = mapped_column(String(80), unique=True, index=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)

    blogs = relationship("Blog", secondary="blog_tags", back_populates="tags")
