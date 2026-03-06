from dataclasses import dataclass
from datetime import datetime
from alembic_utils.pg_policy import PGPolicy
from dataclasses_jsonschema import JsonSchemaMixin
from sqlalchemy.orm import Mapped

from node_agent.model.db import (
    Base,
    column_foreign_key_required_cascade,
    intpk,
    column_id,
    column_string_null,
    column_relationship,
    column_time_created,
    column_time_updated,
)


@dataclass
class ServerPort(Base, JsonSchemaMixin):

    __tablename__ = "server_port"
    id: Mapped[intpk] = column_id()
    server_host_id: Mapped[int] = column_foreign_key_required_cascade(
        "server_host.id"
    )
    time_create: Mapped[datetime] = column_time_created()
    time_updated: Mapped[datetime] = column_time_updated()

    port: Mapped[str] = column_string_null()
    description: Mapped[str] = column_string_null()

    server_host: Mapped["ServerHost"] = column_relationship()  # type: ignore


server_port_select_policy = PGPolicy(
    schema="public",
    signature="server_port_select_org_member",  # policy name only
    on_entity="public.server_port",  # target table
    definition="""
        AS PERMISSIVE
        FOR SELECT
        TO authenticated
        USING (public.is_server_host_member(server_host_id))
    """,
)
