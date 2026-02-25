from dataclasses import dataclass
from datetime import datetime
from alembic_utils.pg_policy import PGPolicy
from sqlalchemy import Table, Column, ForeignKey, Integer
from sqlalchemy.orm import Mapped
from node_agent.model.db import (
    Base,
    intpk,
    column_id,
    column_name,
    column_time_created,
    column_time_updated,
    column_foreign_key,
    column_relationship,
)

# Table d'association many-to-many User <-> Group
user_group_association = Table(
    "user_group_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("group_id", Integer, ForeignKey("group.id"), primary_key=True),
)


@dataclass
class Group(Base):
    __tablename__ = "group"
    id: Mapped[intpk] = column_id()
    time_create: Mapped[datetime] = column_time_created()
    time_updated: Mapped[datetime] = column_time_updated()
    name: Mapped[str] = column_name()
    organisation_id: Mapped[int] = column_foreign_key("organisation.id")
    organisation: Mapped["Organisation"] = column_relationship()  # type: ignore


group_select_policy = PGPolicy(
    schema="public",
    signature="group_select",
    on_entity="public.group",
    definition="""
        AS PERMISSIVE
        FOR SELECT
        TO authenticated
        USING (public.is_org_member(organisation_id))
    """,
)

user_group_association_select_policy = PGPolicy(
    schema="public",
    signature="user_group_association_select",
    on_entity="public.user_group_association",
    definition="""
        AS PERMISSIVE
        FOR SELECT
        TO authenticated
        USING (public.is_group_org_member(group_id))
    """,
)
