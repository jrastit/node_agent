from dataclasses_jsonschema import JsonSchemaMixin
from sqlalchemy.orm import Mapped

from node_agent.model.db import Base, column_string_null, column_foreign_key, \
    column_relationship_list, column_relationship
from node_agent.model.oasis.node import OasisNode


class Entrypoint(Base, JsonSchemaMixin):
    __tablename__ = 'entrypoint'

    user: Mapped[str] = column_string_null()
    path: Mapped[str] = column_string_null()
    ssh_id: Mapped[str] = column_string_null()

    server_id: Mapped[int] = column_foreign_key("server.id")
    server: Mapped['Server'] = column_relationship()

    node = column_relationship_list(
        OasisNode, back_populates="entrypoint",
        foreign_keys="OasisNode.entrypoint_id",
    )
    node_admin = column_relationship_list(
        OasisNode, back_populates="entrypoint_admin",
        foreign_keys="OasisNode.entrypoint_admin_id",
    )