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
from node_agent.model.server import (
    Server,
)  # Needed for runtime type-hint resolution


@dataclass
class ServerHost(Base, JsonSchemaMixin):

    __tablename__ = "server_host"
    id: Mapped[intpk] = column_id()
    server_id: Mapped[int] = column_foreign_key_required_cascade("server.id")
    time_create: Mapped[datetime] = column_time_created()
    time_updated: Mapped[datetime] = column_time_updated()

    name: Mapped[str] = column_string_null()
    description: Mapped[str] = column_string_null()

    server: Mapped["Server"] = column_relationship()  # type: ignore


server_host_select_policy = PGPolicy(
    schema="public",
    signature="server_host_select_org_member",  # policy name only
    on_entity="public.server_host",  # target table
    definition="""
        AS PERMISSIVE
        FOR SELECT
        TO authenticated
        USING (public.is_server_member(server_id))
    """,
)
