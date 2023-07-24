from node_agent.model.db import Base, column_relationship_list
from node_agent.model.oasis.node import OasisNode


class OasisEntity(Base):
    __tablename__ = 'oasis_entity'

    node = column_relationship_list(
        OasisNode,
        back_populates="entity"
    )
