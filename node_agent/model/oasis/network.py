from sqlalchemy.orm import Mapped

from node_agent.model.db import Base, column_string_null, column_relationship_list
from node_agent.model.oasis.nodetype import OasisNodetype


class OasisNetwork(Base):
    __tablename__ = 'oasis_network'

    core_version: Mapped[str] = column_string_null()
    genesis_url: Mapped[str] = column_string_null()
    seed_node: Mapped[str] = column_string_null()

    nodetype = column_relationship_list(
        OasisNodetype,
        back_populates="network",
    )
