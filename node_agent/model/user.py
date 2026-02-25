from dataclasses import dataclass
from datetime import datetime
import uuid
from alembic_utils.pg_policy import PGPolicy
from sqlalchemy.orm import Mapped, relationship
from node_agent.model.db import (
    Base,
    column_uuid,
    intpk,
    column_id,
    column_time_created,
    column_time_updated,
)
from node_agent.model.group import user_group_association


@dataclass
class User(Base):
    __tablename__ = "user"
    id: Mapped[intpk] = column_id()
    auth_user_id: Mapped[uuid.UUID] = column_uuid()

    groups: Mapped[list["Group"]] = relationship(  # type: ignore
        "Group",
        secondary=user_group_association,
    )
    time_create: Mapped[datetime] = column_time_created()
    time_updated: Mapped[datetime] = column_time_updated()


user_select_policy = PGPolicy(
    schema="public",
    signature="user_select",
    on_entity="public.user",
    definition="""
        AS PERMISSIVE
        FOR SELECT
        TO authenticated
        USING (public.is_user())
    """,
)
