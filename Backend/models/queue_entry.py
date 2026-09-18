from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base

if TYPE_CHECKING:
    from models.queue import Queue
    from models.service_session import ServiceSession


class QueueEntry(Base):
    __tablename__ = "queue_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    queue_id: Mapped[int] = mapped_column(ForeignKey("queues.id"))
    service_session: Mapped["ServiceSession | None"] = relationship(
        back_populates="queue_entry"
    )
    user_id: Mapped[int]
    token_number: Mapped[int]
    status: Mapped[str] = mapped_column(String(20), default="waiting")
    queue: Mapped["Queue"] = relationship(back_populates="entries")
