from sqlalchemy.orm import Mapped

from node_agent.model.db import (
    Base,
    # column_relationship_many_to_many,
    intpk,
    column_name,
    column_string_null,
    column_foreign_key,
    column_relationship,
)
from sqlalchemy.orm import Mapped
from node_agent.model.db import (
    column_id,
    column_time_created,
    column_time_updated,
)
from datetime import datetime

# from node_agent.model.oasis.node import node_nodetype


class OasisNodetype(Base):
    __tablename__ = "oasis_nodetype"
    id: Mapped[intpk] = column_id()
    time_create: Mapped[datetime] = column_time_created()
    time_updated: Mapped[datetime] = column_time_updated()

    name: Mapped[str] = column_name()

    core_version: Mapped[str] = column_string_null()
    runtime_identifier: Mapped[str] = column_string_null()
    runtime_version: Mapped[str] = column_string_null()
    runtime_version_old: Mapped[str] = column_string_null()
    runtime_ias: Mapped[str] = column_string_null()
    latest_time_error: Mapped[str] = column_string_null()
    paratime_worker_client_port: Mapped[str] = column_string_null()
    paratime_worker_p2p_port: Mapped[str] = column_string_null()
    node_ssh_id: Mapped[str] = column_string_null()

    network_id: Mapped[int] = column_foreign_key("oasis_network.id")
    network: Mapped["OasisNetwork"] = column_relationship()

    # node: Mapped[list["OasisNode"]] = column_relationship_many_to_many(
    #     "OasisNode",
    #     secondary=node_nodetype,
    #     back_populates="nodetype",
    # )
