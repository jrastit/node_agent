import logging

from sqlalchemy.orm import make_transient

from node_agent.model.oasis.entity import OasisEntity
from node_agent.model.entrypoint import Entrypoint
from node_agent.model.oasis.network import OasisNetwork
from node_agent.model.server import Server
from node_agent.model.oasis.node import OasisNode
from node_agent.model.oasis.nodetype import OasisNodetype
from node_agent.model.db import db
from tests.utils.user_util import user_util_get_test_organization

logger = logging.getLogger(__name__)


def test_db(fastapi_app):
    _, _, organization = user_util_get_test_organization()
    assert organization is not None
    assert organization["id"] is not None
    logger.info(f"Test organization created with ID: {organization['id']}")
    server = Server(
        name="test_server", ip="127.0.0.1", organization_id=organization["id"]
    )
    db.session.add(server)
    db.session.commit()
    entrypoint = Entrypoint(
        name="test_oasis",
        path="/oasis",
        user="oasis",
        server_id=server.id,
    )
    db.session.add(entrypoint)
    db.session.commit()
    db_entrypoint = (
        db.session.query(Entrypoint)
        .filter(Entrypoint.id == entrypoint.id)
        .first()
    )
    assert db_entrypoint is not None
    assert db_entrypoint.server is not None
    admin_entrypoint = Entrypoint(
        name="test_admin",
        path="/oasis",
        user="oasis",
        server_id=server.id,
    )

    db.session.add(admin_entrypoint)
    entity = OasisEntity(
        name="test_entity",
    )
    db.session.add(entity)
    network = OasisNetwork(name="test")
    db.session.add(network)
    nodetype = OasisNodetype(
        name="test_type",
    )
    db.session.add(nodetype)
    db.session.flush()
    node = OasisNode(
        name="test_node",
        entrypoint_id=entrypoint.id,
        entrypoint_admin_id=admin_entrypoint.id,
        entity_id=entity.id,
        nodetype=[nodetype],
    )
    db.session.add(node)
    db.session.commit()
    db_node = (
        db.session.query(OasisNode).filter(OasisNode.id == node.id).first()
    )
    assert db_node is not None
    assert db_node.entrypoint_id is not None
    assert db_node.entrypoint is not None
    assert db_node.entrypoint.server is not None
    assert db_node.entrypoint_admin.server is not None

    db.session.delete(server)
    db.session.commit()
    db_node = (
        db.session.query(OasisNode).filter(OasisNode.id == node.id).first()
    )
    assert db_node is not None
    assert db_node.entrypoint is not None
    assert db_node.entrypoint.server is not None
    assert db_node.entrypoint_admin.server is not None

    make_transient(server)
    db.session.add(server)
    node.entrypoint.server = server
    node.entrypoint_admin.server = server
    db.session.commit()

    db_node = (
        db.session.query(OasisNode).filter(OasisNode.id == node.id).first()
    )
    assert db_node is not None
    assert db_node.entrypoint is not None
    assert db_node.entrypoint.server is not None
    assert db_node.entrypoint_admin.server is not None
