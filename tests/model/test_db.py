from sqlalchemy.orm import make_transient

from node_agent.model.oasis.entity import OasisEntity
from node_agent.model.entrypoint import Entrypoint
from node_agent.model.oasis.network import OasisNetwork
from node_agent.model.server import Server
from node_agent.model.oasis.node import OasisNode
from node_agent.model.oasis.nodetype import OasisNodetype
from node_agent.model.db import db


def test_db(app):
    server = Server(
        name='test_server',
        ip='34.155.3.8'
    )
    app.app_context()
    db.session.add(server)
    entrypoint = Entrypoint(
        name='test_oasis',
        path='/oasis',
        user='oasis',
        server=server,
    )
    db.session.add(entrypoint)
    db.session.commit()
    db_entrypoint = db.session.query(Entrypoint).get(entrypoint.id)
    assert db_entrypoint is not None
    assert db_entrypoint.server is not None
    admin_entrypoint = Entrypoint(
        name='test_admin',
        path='/oasis',
        user='oasis',
        server=server,
    )

    db.session.add(admin_entrypoint)
    entity = OasisEntity(
        name='test_entity',
    )
    db.session.add(entity)
    network = OasisNetwork(
        name='test'
    )
    db.session.add(network)
    nodetype = OasisNodetype(
        name='test_type',
    )
    db.session.add(nodetype)
    node = OasisNode(
        name='test_node',
        entrypoint=entrypoint,
        entrypoint_admin=admin_entrypoint,
        entity=entity,
        nodetype=nodetype,
    )
    db.session.add(node)
    db.session.commit()
    db_node = db.session.query(OasisNode).filter(OasisNode.name == 'test_node').first()
    assert db_node is not None
    assert db_node.entrypoint_id is not None
    assert db_node.entrypoint is not None
    assert db_node.entrypoint.server is not None
    assert db_node.entrypoint_admin.server is not None

    db.session.delete(server)
    db.session.commit()
    db_node = db.session.query(OasisNode).filter(OasisNode.name=='test_node').first()
    assert db_node is not None
    assert db_node.entrypoint is not None
    assert db_node.entrypoint.server is None
    assert db_node.entrypoint_admin.server is None

    make_transient(server)
    db.session.add(server)
    node.entrypoint.server = server
    node.entrypoint_admin.server = server
    db.session.commit()

    db_node = db.session.query(OasisNode).filter(OasisNode.name=='test_node').first()
    assert db_node is not None
    assert db_node.entrypoint is not None
    assert db_node.entrypoint.server is not None
    assert db_node.entrypoint_admin.server is not None
