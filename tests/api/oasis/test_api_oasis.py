from tests.utils.api_util import (
    api_put_data,
)
from tests.utils.test_node import load_test_node


def test_api_oasis_node_post_error(fastapi_app):
    ret = api_put_data("/api/oasis/node", 500, {"error": False})
    assert ret is None
    ret = api_put_data("/api/oasis/nodetype", 500, {"error": False})
    assert ret is None
    ret = api_put_data("/api/oasis/network", 500, {"error": False})
    assert ret is None
    ret = api_put_data("/api/oasis/entity", 500, {"error": False})
    assert ret is None


def test_api_oasis_node(fastapi_app):
    entity_handler = api_put_data(
        "/api/oasis/entity",
        200,
        {
            "name": "test_entity_api",
        },
    )
    assert "OasisEntity" in entity_handler
    entity = entity_handler["OasisEntity"]
    assert "id" in entity
    entity_id = entity["id"]
    assert "name" in entity
    assert entity["name"] == "test_entity_api"

    network_handler = api_put_data(
        "/api/oasis/network",
        200,
        {
            "name": "test_network_api",
        },
    )
    assert "OasisNetwork" in network_handler
    network = network_handler["OasisNetwork"]
    assert "id" in network
    network_id = network["id"]
    assert "name" in network
    assert network["name"] == "test_network_api"

    node_type_handler = api_put_data(
        "/api/oasis/nodetype",
        200,
        {
            "name": "test_nodetype_api",
            "network_id": network_id,
        },
    )
    assert "OasisNodetype" in node_type_handler
    node_type = node_type_handler["OasisNodetype"]
    assert "id" in node_type
    node_type_id = node_type["id"]
    assert "name" in node_type
    assert node_type["name"] == "test_nodetype_api"

    node_handler = api_put_data(
        "/api/oasis/node",
        200,
        {
            "name": "test_node_api",
            "entity_id": entity_id,
            "nodetype_id": [node_type_id],
        },
    )
    assert "OasisNode" in node_handler
    node = node_handler["OasisNode"]
    assert "id" in node
    node_id = node["id"]
    assert node_id is not None
    assert "name" in node
    assert node["name"] == "test_node_api"
    assert node["entity_id"] == entity_id
    assert len(node["nodetype"]) == 1

    node_handler = api_put_data(
        "/api/oasis/node",
        200,
        {
            "id": node_id,
            "name": "test_node_api",
            "entity_id": entity_id,
            "nodetype_id": [node_type_id],
        },
    )
    assert "OasisNode" in node_handler
    node = node_handler["OasisNode"]
    assert "id" in node
    node_id = node["id"]
    assert node_id is not None
    assert "name" in node
    assert node["name"] == "test_node_api"
    assert node["entity_id"] == entity_id
    assert len(node["nodetype"]) == 1

    node_handler = api_put_data(
        "/api/oasis/node",
        200,
        {
            "id": node_id,
            "name": "test_node_api",
            "entity_id": entity_id,
        },
    )
    assert "OasisNode" in node_handler
    node = node_handler["OasisNode"]
    assert "id" in node
    node_id = node["id"]
    assert node_id is not None
    assert "name" in node
    assert node["name"] == "test_node_api"
    assert node["entity_id"] == entity_id
    assert len(node["nodetype"]) == 0

    node_handler = api_put_data(
        "/api/oasis/node",
        200,
        {
            "id": node_id,
            "name": "test_node_api",
            "entity_id": entity_id,
            "nodetype_id": [node_type_id],
        },
    )
    assert "OasisNode" in node_handler
    node = node_handler["OasisNode"]
    assert "id" in node
    node_id = node["id"]
    assert node_id is not None
    assert "name" in node
    assert node["name"] == "test_node_api"
    assert node["entity_id"] == entity_id
    assert len(node["nodetype"]) == 1


def test_api_oasis_node_save(fastapi_app):
    load_test_node()
    api_put_data("/api/oasis/config/save", 200, {})
