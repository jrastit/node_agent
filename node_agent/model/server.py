from dataclasses import dataclass
from datetime import datetime

from node_agent.model.db import (
    Base,
    column_name,
    intpk,
    column_id,
    column_string_null,
    column_relationship_list,
    column_time_created,
    column_time_updated,
    column_foreign_key,
    column_relationship,
)
from node_agent.model.entrypoint import Entrypoint

from sqlalchemy.orm import Mapped


@dataclass
class Server(Base):

    __tablename__ = "server"
    id: Mapped[intpk] = column_id()
    time_create: Mapped[datetime] = column_time_created()
    time_updated: Mapped[datetime] = column_time_updated()

    name: Mapped[str] = column_name()

    cloud: Mapped[str] = column_string_null()
    cloud_name: Mapped[str] = column_string_null()
    ip: Mapped[str] = column_string_null()

    entrypoint: Mapped[list[Entrypoint]] = column_relationship_list(
        Entrypoint,
        back_populates="server",
    )

    organisation_id: Mapped[int] = column_foreign_key("organisation.id")
    organisation: Mapped["Organisation"] = column_relationship()  # type: ignore

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "cloud": self.cloud,
            "cloud_name": self.cloud_name,
            "ip": self.ip,
            "time_create": (
                self.time_create.isoformat() if self.time_create else None
            ),
            "time_updated": (
                self.time_updated.isoformat() if self.time_updated else None
            ),
            "organisation_id": self.organisation_id,
        }
