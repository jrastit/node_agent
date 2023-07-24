from dataclasses import dataclass

from dataclasses_jsonschema import JsonSchemaMixin

from node_agent.model.db import Base, column_string_null, column_relationship_list
from node_agent.model.entrypoint import Entrypoint

from sqlalchemy.orm import Mapped


@dataclass
class Server(Base, JsonSchemaMixin):
    __tablename__ = 'server'

    cloud: Mapped[str] = column_string_null()
    cloud_name: Mapped[str] = column_string_null()
    ip: Mapped[str] = column_string_null()

    entrypoint = column_relationship_list(
        Entrypoint,
        back_populates="server",
    )
