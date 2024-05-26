from datetime import datetime
from sqlalchemy.orm import Mapped

from node_agent.model.db import (
    Base,
    intpk,
    column_id,
    column_name,
    column_relationship_list,
    column_string_null,
    column_time_created,
    column_time_updated,
    column_bool_null,
)
from node_agent.model.oasis.node import OasisNode


class OasisConfig(Base):
    __tablename__ = "oasis_config"
    id: Mapped[intpk] = column_id()
    time_create: Mapped[datetime] = column_time_created()
    time_updated: Mapped[datetime] = column_time_updated()

    md5: Mapped[str] = column_string_null()

    network: Mapped[str] = column_string_null()
    network_genesis_file: Mapped[str] = column_string_null()
    network_seed_node: Mapped[str] = column_string_null()
    network_core_version: Mapped[str] = column_string_null()
    network_core_version_url: Mapped[str] = column_string_null()

    validate: Mapped[bool] = column_bool_null()


class OasisParatimeConfig(Base):
    __tablename__ = "oasis_paratime_config"
    id: Mapped[intpk] = column_id()
    time_create: Mapped[datetime] = column_time_created()
    time_updated: Mapped[datetime] = column_time_updated()

    name: Mapped[str] = column_name()
    core_version: Mapped[str] = column_string_null()
    core_version_url: Mapped[str] = column_string_null()
    runtime_identifier: Mapped[str] = column_string_null()
    runtime_version: Mapped[str] = column_string_null()
    runtime_version_url: Mapped[str] = column_string_null()
    IAS_proxy: Mapped[str] = column_string_null()

    oasis_config_id: Mapped[int] = column_id()
    oasis_config = column_relationship_list(
        OasisConfig, back_populates="oasis_paratime_config"
    )
