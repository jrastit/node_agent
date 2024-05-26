from sqlalchemy.orm import Mapped

from node_agent.model.db import (
    Base,
    column_relationship_list,
    column_string_null,
)
from node_agent.model.oasis.node import OasisNode


class OasisEntity(Base):
    __tablename__ = "oasis_entity"
    entity_id: Mapped[str] = column_string_null()

    node = column_relationship_list(OasisNode, back_populates="entity")
