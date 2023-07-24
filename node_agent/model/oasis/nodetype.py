from sqlalchemy.orm import Mapped

from node_agent.model.db import Base, column_string_null, column_foreign_key, \
    column_relationship_list, column_relationship
from node_agent.model.oasis.node import OasisNode


class OasisNodetype(Base):
    __tablename__ = 'oasis_nodetype'

    core_version: Mapped[str] = column_string_null()
    runtime_identifier: Mapped[str] = column_string_null()
    runtime_version: Mapped[str] = column_string_null()
    runtime_version_old: Mapped[str] = column_string_null()
    runtime_ias: Mapped[str] = column_string_null()
    latest_time_error: Mapped[str] = column_string_null()
    paratime_worker_client_port: Mapped[str] = column_string_null()
    paratime_worker_p2p_port: Mapped[str] = column_string_null()
    node_ssh_id: Mapped[str] = column_string_null()

    network_id: Mapped[int] = column_foreign_key(
        "oasis_network.id")
    network: Mapped["OasisNetwork"] = column_relationship()

    node = column_relationship_list(
        OasisNode,
        back_populates="nodetype"
    )
