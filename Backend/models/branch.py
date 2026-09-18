from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base

if TYPE_CHECKING:
    from models.organization import Organization
    from models.service import Service


class Branch(Base):
    __tablename__ = "branches"

    id: Mapped[int] = mapped_column(primary_key=True)

    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))

    name: Mapped[str] = mapped_column(String(100))

    status: Mapped[str] = mapped_column(String(20), default="active")

    organization: Mapped["Organization"] = relationship(back_populates="branches")

    services: Mapped[list["Service"]] = relationship(back_populates="branch")
