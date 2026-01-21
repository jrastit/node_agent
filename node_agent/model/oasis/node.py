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
    entity: Mapped["OasisEntity"] = column_relationship()  # type: ignore
    entrypoint_id: Mapped[int] = column_foreign_key("entrypoint.id")
    entrypoint: Mapped["Entrypoint"] = column_relationship(  # type: ignore
        foreign_keys="OasisNode.entrypoint_id"
    )
    entrypoint_admin_id: Mapped[int] = column_foreign_key("entrypoint.id")
    entrypoint_admin: Mapped["Entrypoint"] = column_relationship(  # type: ignore
        foreign_keys="OasisNode.entrypoint_admin_id"
    )

    nodetype: Mapped[list["OasisNodetype"]] = column_relationship_many_to_many(  # type: ignore
        "OasisNodetype",
        secondary=node_nodetype,
        # back_populates="node",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "core_version": self.core_version,
            "genesis_url": self.genesis_url,
            "seed_node": self.seed_node,
            "node_root_dir": self.node_root_dir,
            "node_address": self.node_address,
            "node_port": self.node_port,
            "paratime_worker_client_port": self.paratime_worker_client_port,
            "paratime_worker_p2p_port": self.paratime_worker_p2p_port,
            "node_id": self.node_id,
            "entity_id": self.entity_id,
            "entrypoint_id": self.entrypoint_id,
            "entrypoint": (
                self.entrypoint.to_dict() if self.entrypoint else None
            ),
            "entrypoint_admin_id": self.entrypoint_admin_id,
            "entrypoint_admin": (
                self.entrypoint_admin.to_dict()
                if self.entrypoint_admin
                else None
            ),
            "nodetype": (
                [nt.to_dict() for nt in self.nodetype] if self.nodetype else []
            ),
            "time_create": (
                self.time_create.isoformat() if self.time_create else None
            ),
            "time_updated": (
                self.time_updated.isoformat() if self.time_updated else None
            ),
        }
