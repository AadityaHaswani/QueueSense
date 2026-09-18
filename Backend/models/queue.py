from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base

if TYPE_CHECKING:
    from models.queue_entry import QueueEntry
    from models.service import Service


class Queue(Base):
    __tablename__ = "queues"

    id: Mapped[int] = mapped_column(primary_key=True)

    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))

    name: Mapped[str] = mapped_column(String(100))

    status: Mapped[str] = mapped_column(String(20), default="active")

    current_token: Mapped[int] = mapped_column(default=0)

    service: Mapped["Service"] = relationship(back_populates="queues")

    entries: Mapped[list["QueueEntry"]] = relationship(back_populates="queue")
