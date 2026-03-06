from dataclasses import dataclass
from datetime import datetime

from alembic_utils.pg_policy import PGPolicy

from node_agent.model.db import (
    Base,
    column_name,
    db,
    intpk,
    column_id,
    column_string_null,
    column_time_created,
    column_time_updated,
    column_foreign_key_required_cascade,
    column_relationship,
)

from sqlalchemy.orm import Mapped, mapped_column


@dataclass
class Server(Base):

    __tablename__ = "server"
    id: Mapped[intpk] = column_id()

    organization_id: Mapped[int] = column_foreign_key_required_cascade(
        "organization.id"
    )

    time_create: Mapped[datetime] = column_time_created()
    time_updated: Mapped[datetime] = column_time_updated()

    name: Mapped[str] = column_name()

    cloud: Mapped[str] = column_string_null()
    cloud_name: Mapped[str] = column_string_null()
    ip: Mapped[str] = column_string_null()
    hostname: Mapped[str] = column_string_null()
    fqdn: Mapped[str] = column_string_null()
    os: Mapped[str] = column_string_null()
    kernel: Mapped[str] = column_string_null()
    cpu_cores: Mapped[int | None] = mapped_column(
        db.Integer, nullable=True, default=None
    )
    ram_total_mb: Mapped[int | None] = mapped_column(
        db.Integer, nullable=True, default=None
    )

    organization: Mapped["Organization"] = column_relationship()  # type: ignore


server_select_policy = PGPolicy(
    schema="public",
    signature="server_select_org_member",  # policy name only
    on_entity="public.server",  # target table
    definition="""
        AS PERMISSIVE
        FOR SELECT
        TO authenticated
        USING (public.is_org_member(organization_id))
    """,
)
