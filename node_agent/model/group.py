
from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import Table, Column, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship
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

# Table d'association many-to-many User <-> Group
user_group_association = Table(
    "user_group_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("group_id", Integer, ForeignKey("group.id"), primary_key=True),
)

@dataclass
class Group(Base):
    __tablename__ = "group"
    id: Mapped[intpk] = column_id()
    users: Mapped[list["User"]] = relationship( # type: ignore
        "User",
        secondary=user_group_association,
        back_populates="groups",
    ) 
    time_create: Mapped[datetime] = column_time_created()
    time_updated: Mapped[datetime] = column_time_updated()
    name: Mapped[str] = column_name()
    organisation_id: Mapped[int] = column_foreign_key("organisation.id")
    organisation: Mapped["Organisation"] = column_relationship() # type: ignore
    
