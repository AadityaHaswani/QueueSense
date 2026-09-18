from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base

if TYPE_CHECKING:
    from models.branch import Branch


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100))

    status: Mapped[str] = mapped_column(String(20), default="active")

    branches: Mapped[list["Branch"]] = relationship(back_populates="organization")
