from dataclasses import dataclass
from datetime import datetime

from alembic_utils.pg_policy import PGPolicy

from node_agent.model.db import (
    Base,
    column_name,
    intpk,
    column_id,
    column_string_null,
    column_time_created,
    column_time_updated,
    column_foreign_key,
    column_relationship,
)
from node_agent.model.entrypoint import Entrypoint

from sqlalchemy.orm import Mapped


@dataclass
class Server(Base):

    __tablename__ = "server"
    id: Mapped[intpk] = column_id()
    time_create: Mapped[datetime] = column_time_created()
    time_updated: Mapped[datetime] = column_time_updated()

    name: Mapped[str] = column_name()

    cloud: Mapped[str] = column_string_null()
    cloud_name: Mapped[str] = column_string_null()
    ip: Mapped[str] = column_string_null()

    organisation_id: Mapped[int] = column_foreign_key("organisation.id")
    organisation: Mapped["Organisation"] = column_relationship()  # type: ignore


server_select_policy = PGPolicy(
    schema="public",
    signature="server_select_org_member",  # policy name only
    on_entity="public.server",  # target table
    definition="""
        AS PERMISSIVE
        FOR SELECT
        TO authenticated
        USING (public.is_org_member(organisation_id))
    """,
)
