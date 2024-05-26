from typing import List
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import Mapped
from datetime import datetime

from node_agent.model.db import (
    Base,
    intpk,
    column_foreign_key,
    column_id,
    column_name,
    column_relationship,
    column_string_null,
    column_relationship_many_to_many,
    column_time_created,
    column_time_updated,
)

from node_agent.model.oasis.nodetype import OasisNodetype

node_nodetype = Table(
    "oasis_node_nodetype",
    Base.metadata,
    Column(
        "node_id",
        Integer,
        ForeignKey("oasis_node.id"),
        primary_key=True,
    ),
    Column(
        "nodetype_id",
        Integer,
        ForeignKey("oasis_nodetype.id"),
        primary_key=True,
    ),
)


class OasisNode(Base):
    __tablename__ = "oasis_node"
    id: Mapped[intpk] = column_id()
    time_create: Mapped[datetime] = column_time_created()
    time_updated: Mapped[datetime] = column_time_updated()

    name: Mapped[str] = column_name()

    core_version: Mapped[str] = column_string_null()
    genesis_url: Mapped[str] = column_string_null()
    seed_node: Mapped[str] = column_string_null()
    node_root_dir: Mapped[str] = column_string_null()
    node_address: Mapped[str] = column_string_null()
    node_port: Mapped[str] = column_string_null()
    paratime_worker_client_port: Mapped[str] = column_string_null()
    paratime_worker_p2p_port: Mapped[str] = column_string_null()

    node_id: Mapped[str] = column_string_null()

    entity_id: Mapped[int] = column_foreign_key("oasis_entity.id")
    entity: Mapped["OasisEntity"] = column_relationship()
    entrypoint_id: Mapped[int] = column_foreign_key("entrypoint.id")
    entrypoint: Mapped["Entrypoint"] = column_relationship(
        foreign_keys="OasisNode.entrypoint_id"
    )
    entrypoint_admin_id: Mapped[int] = column_foreign_key("entrypoint.id")
    entrypoint_admin: Mapped["Entrypoint"] = column_relationship(
        foreign_keys="OasisNode.entrypoint_admin_id"
    )

    nodetype: Mapped[list["OasisNodetype"]] = column_relationship_many_to_many(
        OasisNodetype,
        secondary=node_nodetype,
    )
