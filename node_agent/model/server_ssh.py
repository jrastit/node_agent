from dataclasses import dataclass
from datetime import datetime
from alembic_utils.pg_policy import PGPolicy
from dataclasses_jsonschema import JsonSchemaMixin
from sqlalchemy.orm import Mapped

from node_agent.model.db import (
    Base,
    intpk,
    column_id,
    column_string_null,
    column_foreign_key_required_cascade,
    column_relationship,
    column_time_created,
    column_time_updated,
)


@dataclass
class ServerSSH(Base, JsonSchemaMixin):

    __tablename__ = "server_ssh"
    id: Mapped[intpk] = column_id()
    server_port_id: Mapped[int] = column_foreign_key_required_cascade(
        "server_port.id"
    )
    time_create: Mapped[datetime] = column_time_created()
    time_updated: Mapped[datetime] = column_time_updated()

    user_name: Mapped[str] = column_string_null()
    description: Mapped[str] = column_string_null()

    server_port: Mapped["ServerPort"] = column_relationship()  # type: ignore


server_ssh_select_policy = PGPolicy(
    schema="public",
    signature="server_ssh_select_org_member",  # policy name only
    on_entity="public.server_ssh",  # target table
    definition="""
        AS PERMISSIVE
        FOR SELECT
        TO authenticated
        USING (public.is_server_port_member(server_port_id))
    """,
)
