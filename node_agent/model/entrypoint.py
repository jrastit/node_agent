from datetime import datetime
from dataclasses_jsonschema import JsonSchemaMixin
from sqlalchemy.orm import Mapped

from node_agent.model.db import (
    Base,
    intpk,
    column_id,
    column_string_null,
    column_foreign_key,
    column_relationship_list,
    column_relationship,
    column_time_created,
    column_time_updated,
)
from node_agent.model.oasis.node import OasisNode


class Entrypoint(Base, JsonSchemaMixin):
    __tablename__ = "entrypoint"
    id: Mapped[intpk] = column_id()
    time_create: Mapped[datetime] = column_time_created()
    time_updated: Mapped[datetime] = column_time_updated()

    name: Mapped[str] = column_string_null()
    user: Mapped[str] = column_string_null()
    path: Mapped[str] = column_string_null()
    ssh_id: Mapped[str] = column_string_null()

    server_id: Mapped[int] = column_foreign_key("server.id")
    server: Mapped["Server"] = column_relationship() # type: ignore

    node = column_relationship_list(
        OasisNode,
        back_populates="entrypoint",
        foreign_keys="OasisNode.entrypoint_id",
    )
    node_admin = column_relationship_list(
        OasisNode,
        back_populates="entrypoint_admin",
        foreign_keys="OasisNode.entrypoint_admin_id",
    )
