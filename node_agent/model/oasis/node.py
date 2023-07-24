from sqlalchemy.orm import Mapped

from node_agent.model.db import Base, column_foreign_key, column_string_null, \
    column_relationship


class OasisNode(Base):
    __tablename__ = 'oasis_node'

    core_version: Mapped[str] = column_string_null()
    genesis_url: Mapped[str] = column_string_null()
    seed_node: Mapped[str] = column_string_null()
    node_root_dir: Mapped[str] = column_string_null()
    node_address: Mapped[str] = column_string_null()
    node_port: Mapped[str] = column_string_null()
    paratime_worker_client_port: Mapped[str] = column_string_null()
    paratime_worker_p2p_port: Mapped[str] = column_string_null()

    entity_id: Mapped[int] = column_foreign_key("oasis_entity.id")
    entity: Mapped['OasisEntity'] = column_relationship()
    nodetype_id: Mapped[int] = column_foreign_key("oasis_nodetype.id")
    nodetype: Mapped['OasisNodetype'] = column_relationship()
    entrypoint_id: Mapped[int] = column_foreign_key("entrypoint.id")
    entrypoint: Mapped['Entrypoint'] = column_relationship(foreign_keys="OasisNode.entrypoint_id")
    entrypoint_admin_id: Mapped[int] = column_foreign_key("entrypoint.id")
    entrypoint_admin: Mapped['Entrypoint'] = column_relationship(foreign_keys="OasisNode.entrypoint_admin_id")
