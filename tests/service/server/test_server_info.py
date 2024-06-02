import logging
from tests.utils.test_node import load_test_node
from node_agent.service.server.server_info import server_get_public_address
from node_agent.service.server.server_install import server_install_package

logger = logging.getLogger()


def test_server_info_status(app):
    node = load_test_node()
    assert "id" in node
    server_install_package("curl", node["entrypoint_admin"])
    # status = oasis_node_info_status(node)
    # assert status is not None
    # status = oasis_node_info(node)
    # logger.info(status)
    status = server_get_public_address(node["entrypoint"])
    logger.info(status)
