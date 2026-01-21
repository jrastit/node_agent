from dataclasses import asdict
import logging


from node_agent.config import settings
from node_agent.model.db import db
from node_agent.model.oasis.node import OasisNode
from tests.utils.api_util import api_put_data

logger = logging.getLogger()


def load_test_node():

    node_db = (
        db.session.query(OasisNode)
        .filter(OasisNode.name == settings.test_node_name)
        .first()
    )

    if node_db is not None:
        node = asdict(node_db)
        assert node["entrypoint"]["server"]["ip"] == settings.test_node_address
        return node

    server_handler = api_put_data(
        "/api/server",
        200,
        {
            "name": "oasis_test_server",
            "ip": settings.test_node_address,
        },
    )
    assert "Server" in server_handler
    server = server_handler["Server"]
    assert "id" in server
    server_id = server["id"]
    assert "ip" in server
    assert "name" in server
    assert server["ip"] == settings.test_node_address

    entrypoint_handler = api_put_data(
        "/api/server/entrypoint",
        200,
        {
            "name": "oasis_test_entrypoint",
            "path": settings.test_node_root_dir,
            "user": settings.test_user,
            "server_id": server_id,
            "ssh_id": settings.test_ssh_id,
        },
    )
    assert "Entrypoint" in entrypoint_handler
    entrypoint = entrypoint_handler["Entrypoint"]
    assert "id" in entrypoint
    assert "path" in entrypoint
    assert "user" in entrypoint
    assert "server_id" in entrypoint
    assert "ssh_id" in entrypoint
    entrypoint_id = entrypoint["id"]

    entrypoint_admin_handler = api_put_data(
        "/api/server/entrypoint",
        200,
        {
            "name": "oasis_test_entrypoint_admin",
            "path": "/root",
            "user": settings.test_admin_user,
            "server_id": server_id,
        },
    )
    assert "Entrypoint" in entrypoint_admin_handler
    entrypoint_admin = entrypoint_admin_handler["Entrypoint"]
    assert "id" in entrypoint_admin
    entrypoint_admin_id = entrypoint_admin["id"]

    network_handler = api_put_data(
        "/api/oasis/network",
        200,
        {
            "name": settings.test_network,
            "core_version": settings.test_core_version,
            "genesis_url": settings.test_genesis_url,
            "seed_node": settings.test_seed_node,
        },
    )

    assert "OasisNetwork" in network_handler
    network = network_handler["OasisNetwork"]
    assert "id" in network
    network_id = network["id"]

    nodetype_handler = api_put_data(
        "/api/oasis/nodetype",
        200,
        {
            "name": settings.test_node_type,
            "network_id": network_id,
        },
    )

    assert "OasisNodetype" in nodetype_handler
    nodetype = nodetype_handler["OasisNodetype"]
    assert "id" in nodetype
    nodetype_id = nodetype["id"]

    entity_handler = api_put_data(
        "/api/oasis/entity",
        200,
        {
            "name": settings.test_entity,
            "entity_id": settings.test_entity_id,
        },
    )

    assert "OasisEntity" in entity_handler
    entity = entity_handler["OasisEntity"]
    assert "id" in entity
    entity_id = entity["id"]

    node_handler = api_put_data(
        "/api/oasis/node",
        200,
        {
            "name": settings.test_node_name,
            "node_address": settings.test_node_address,
            "node_port": settings.test_node_port,
            "core_version": settings.test_core_version,
            "server_id": server_id,
            "entity_id": entity_id,
            "entrypoint_id": entrypoint_id,
            "entrypoint_admin_id": entrypoint_admin_id,
            "nodetype_id": [nodetype_id],
            "node_port": settings.test_node_port,
            "paratime_worker_client_port": settings.test_paratime_worker_client_port,
            "paratime_worker_p2p_port": settings.test_paratime_worker_p2p_port,
        },
    )

    assert "OasisNode" in node_handler
    node = node_handler["OasisNode"]
    assert "id" in node
    # logger.info(f"Node: {node}")
    return node
