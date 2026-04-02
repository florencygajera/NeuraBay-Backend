from datetime import datetime
from sqlalchemy import String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.base import IDMixin, TimestampMixin, SoftDeleteMixin
from app.models.blog_tag import blog_tags


class Blog(Base, IDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "blogs"

    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    summary: Mapped[str | None] = mapped_column(String(500))
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    author_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))

    author = relationship("User", back_populates="blogs")
    category = relationship("Category", back_populates="blogs")
    tags = relationship("Tag", secondary=blog_tags, back_populates="blogs")

    @property
    def tag_ids(self) -> list[int]:
        return [tag.id for tag in self.tags] if self.tags else []
