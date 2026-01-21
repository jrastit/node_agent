from dataclasses import dataclass
from datetime import datetime
from sqlalchemy.orm import Mapped
from node_agent.model.db import (
    Base,
    intpk,
    column_id,
    column_name,
    column_time_created,
    column_time_updated,
    column_foreign_key,
    column_relationship,
    column_relationship_list,
)


@dataclass
class Organisation(Base):
    __tablename__ = "organisation"
    id: Mapped[intpk] = column_id()
    time_create: Mapped[datetime] = column_time_created()
    time_updated: Mapped[datetime] = column_time_updated()
    name: Mapped[str] = column_name()
    parent_id: Mapped[int] = column_foreign_key(
        "organisation.id", primary_key=False
    )
    parent: Mapped["Organisation"] = column_relationship(
        foreign_keys="Organisation.parent_id"
    )
    groups: Mapped[list["Group"]] = column_relationship_list("Group", back_populates="organisation")  # type: ignore
