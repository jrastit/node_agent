from dataclasses import dataclass
from datetime import datetime
from sqlalchemy.orm import Mapped, relationship
from node_agent.model.db import (
    Base,
    intpk,
    column_id,
    column_name,
    column_string_null,
    column_time_created,
    column_time_updated,
    column_relationship,
    column_foreign_key,
)
from node_agent.model.group import user_group_association


@dataclass
class User(Base):
    __tablename__ = "user"
    id: Mapped[intpk] = column_id()
    groups: Mapped[list["Group"]] = relationship(  # type: ignore
        "Group",
        secondary=user_group_association,
        back_populates="users",
    )
    name: Mapped[str] = column_name()
    email: Mapped[str] = column_string_null()
    organisation_id: Mapped[int] = column_foreign_key("organisation.id")
    organisation: Mapped["Organisation"] = column_relationship()  # type: ignore
    time_create: Mapped[datetime] = column_time_created()
    time_updated: Mapped[datetime] = column_time_updated()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "organisation_id": self.organisation_id,
            "time_create": (
                self.time_create.isoformat() if self.time_create else None
            ),
            "time_updated": (
                self.time_updated.isoformat() if self.time_updated else None
            ),
        }
