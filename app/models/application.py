from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.base import IDMixin, TimestampMixin, SoftDeleteMixin


class Application(Base, IDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "applications"

    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"), index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    resume_url: Mapped[str | None] = mapped_column(String(500))
    cover_letter: Mapped[str | None] = mapped_column(Text)

    job = relationship("Job", back_populates="applications")
