from datetime import datetime
from sqlalchemy.orm import Mapped

from node_agent.model.db import (
    Base,
    intpk,
    column_id,
    column_name,
    column_relationship_list,
    column_string_null,
    column_time_created,
    column_time_updated,
)
from node_agent.model.oasis.node import OasisNode


class OasisEntity(Base):
    __tablename__ = "oasis_entity"
    id: Mapped[intpk] = column_id()
    time_create: Mapped[datetime] = column_time_created()
    time_updated: Mapped[datetime] = column_time_updated()

    name: Mapped[str] = column_name()

    entity_id: Mapped[str] = column_string_null()

    node = column_relationship_list(OasisNode, back_populates="entity")
