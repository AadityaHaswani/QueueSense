from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base

if TYPE_CHECKING:
    from models.queue_entry import QueueEntry


class ServiceSession(Base):
    __tablename__ = "service_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)

    queue_entry_id: Mapped[int] = mapped_column(
        ForeignKey("queue_entries.id")
    )

    started_at: Mapped[datetime] = mapped_column(DateTime)
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    queue_entry: Mapped["QueueEntry"] = relationship(
        back_populates="service_session"
    )