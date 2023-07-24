from node_agent.config import settings
from node_agent.model.db import db
from node_agent.model.oasis.node import OasisNode
from tests.utils.api_util import api_put_data


def load_test_node():

    node = db.session.query(OasisNode).filter(OasisNode.name == 'oasis_test_node').first()

    if node is not None:
        return node

    server_handler = api_put_data(
        '/api/server',
        200,
        {
            "name": "oasis_test_server",
            "ip": settings.test_node_address,
        }
    )
    assert 'Server' in server_handler
    server = server_handler['Server']
    assert 'id' in server
    server_id = server['id']

    entrypoint_handler = api_put_data(
        '/api/server/entrypoint',
        200,
        {
            "name": "oasis_test_entrypoint",
            "path": settings.test_node_root_dir,
            "user": settings.test_user,
            "server_id": server_id,
            "ssh_id": settings.test_ssh_id,
        }
    )
    assert 'Entrypoint' in entrypoint_handler
    entrypoint = entrypoint_handler['Entrypoint']
    assert 'id' in entrypoint
    entrypoint_id = entrypoint['id']

    entrypoint_admin_handler = api_put_data(
        '/api/server/entrypoint',
        200,
        {
            "name": "oasis_test_entrypoint_admin",
            "path": "/root",
            "user": settings.test_admin_user,
            "server_id": server_id,
        }
    )
    assert 'Entrypoint' in entrypoint_admin_handler
    entrypoint_admin = entrypoint_admin_handler['Entrypoint']
    assert 'id' in entrypoint_admin
    entrypoint_admin_id = entrypoint_admin['id']

    network_handler = api_put_data(
        '/api/oasis/network',
        200,
        {
            "name": settings.test_network,
            "core_version": settings.test_core_version,
            "genesis_url": settings.test_genesis_url,
            "seed_node": settings.test_seed_node,
        }
    )

    assert 'OasisNetwork' in network_handler
    network = network_handler['OasisNetwork']
    assert 'id' in network
    network_id = network['id']

    nodetype_handler = api_put_data(
        '/api/oasis/nodetype',
        200,
        {
            "name": settings.test_node_type,
        }
    )

    assert 'OasisNodetype' in nodetype_handler
    nodetype = nodetype_handler['OasisNodetype']
    assert 'id' in nodetype
    nodetype_id = nodetype['id']

    entity_handler = api_put_data(
        '/api/oasis/entity',
        200,
        {
            "name": settings.test_entity,
        }
    )

    assert 'OasisEntity' in entity_handler
    entity = entity_handler['OasisEntity']
    assert 'id' in entity
    entity_id = entity['id']

    node_handler = api_put_data(
        '/api/oasis/node',
        200,
        {
            "name": "oasis_test_node",
            "server_id": server_id,
            "entrypoint_id": entrypoint_id,
            "entrypoint_admin_id": entrypoint_admin_id,
            "node_type": nodetype_id,
            "node_port": settings.test_node_port,
            "paratime_worker_client_port":
                settings.test_paratime_worker_client_port,
            "paratime_worker_p2p_port":
                settings.test_paratime_worker_p2p_port,
        }
    )

    assert 'OasisNode' in node_handler
    node = node_handler['OasisNode']
    assert 'id' in node
    return node
