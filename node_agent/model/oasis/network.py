from datetime import datetime
from sqlalchemy.orm import Mapped

from node_agent.model.db import (
    Base,
    column_name,
    intpk,
    column_id,
    column_time_created,
    column_time_updated,
    column_string_null,
    column_relationship_list,
)
from node_agent.model.oasis.nodetype import OasisNodetype


class OasisNetwork(Base):

    __tablename__ = "oasis_network"
    id: Mapped[intpk] = column_id()
    time_create: Mapped[datetime] = column_time_created()
    time_updated: Mapped[datetime] = column_time_updated()

    name: Mapped[str] = column_name()

    core_version: Mapped[str] = column_string_null()
    genesis_url: Mapped[str] = column_string_null()
    seed_node: Mapped[str] = column_string_null()

    nodetype = column_relationship_list(
        OasisNodetype,
        back_populates="network",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "core_version": self.core_version,
            "genesis_url": self.genesis_url,
            "seed_node": self.seed_node,
            "time_create": (
                self.time_create.isoformat() if self.time_create else None
            ),
            "time_updated": (
                self.time_updated.isoformat() if self.time_updated else None
            ),
        }
