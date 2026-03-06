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
from node_agent.model.server import Server  # Needed for runtime type-hint resolution


@dataclass
class ServerStatus(Base, JsonSchemaMixin):

    __tablename__ = "server_status"
    id: Mapped[intpk] = column_id()
    server_id: Mapped[int] = column_foreign_key_required_cascade("server.id")
    time_create: Mapped[datetime] = column_time_created()
    time_updated: Mapped[datetime] = column_time_updated()

    uptime: Mapped[str] = column_string_null()
    load_avg_1m: Mapped[float] = column_string_null()
    load_avg_5m: Mapped[float] = column_string_null()
    load_avg_15m: Mapped[float] = column_string_null()
    memory_total_mb: Mapped[int] = column_string_null()
    memory_used_mb: Mapped[int] = column_string_null()
    memory_free_mb: Mapped[int] = column_string_null()
    memory_shared_mb: Mapped[int] = column_string_null()
    memory_buff_cache_mb: Mapped[int] = column_string_null()
    memory_available_mb: Mapped[int] = column_string_null()
    swap_total_mb: Mapped[int] = column_string_null()
    swap_used_mb: Mapped[int] = column_string_null()
    swap_free_mb: Mapped[int] = column_string_null()
    health_reachable: Mapped[bool] = column_string_null()
    health_service_active: Mapped[bool] = column_string_null()
    health_service_status_ok: Mapped[bool] = column_string_null()
    collected_at: Mapped[datetime] = column_string_null()

    server: Mapped["Server"] = column_relationship()  # type: ignore


server_status_select_policy = PGPolicy(
    schema="public",
    signature="server_status_select_org_member",  # policy name only
    on_entity="public.server_status",  # target table
    definition="""
        AS PERMISSIVE
        FOR SELECT
        TO authenticated
        USING (public.is_server_member(server_id))
    """,
)
