from dataclasses import dataclass
from datetime import datetime
from alembic_utils.pg_policy import PGPolicy
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


@dataclass
class Organisation(Base):
    __tablename__ = "organisation"
    id: Mapped[intpk] = column_id()
    time_create: Mapped[datetime] = column_time_created()
    time_updated: Mapped[datetime] = column_time_updated()
    name: Mapped[str] = column_name()
    parent_id: Mapped[int] = column_foreign_key(
        "organisation.id", primary_key=False
    )
    parent: Mapped["Organisation"] = column_relationship(
        foreign_keys="Organisation.parent_id"
    )


organisation_select_policy = PGPolicy(
    schema="public",
    signature="organisation_select",
    on_entity="public.organisation",
    definition="""
        AS PERMISSIVE
        FOR SELECT
        TO authenticated
        USING (public.is_org_member(id))
    """,
)
