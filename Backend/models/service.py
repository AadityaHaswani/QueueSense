from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base

if TYPE_CHECKING:
    from models.branch import Branch
    from models.queue import Queue


class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    queues: Mapped[list["Queue"]] = relationship(back_populates="service")

    branch_id: Mapped[int] = mapped_column(ForeignKey("branches.id"))

    name: Mapped[str] = mapped_column(String(100))

    status: Mapped[str] = mapped_column(String(20), default="active")

    branch: Mapped["Branch"] = relationship(back_populates="services")
