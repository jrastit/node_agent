import logging
from tests.utils.test_node import load_test_node
from node_agent.service.oasis.node_info import (
    oasis_node_info,
    oasis_node_info_status,
    oasis_node_status,
)

logger = logging.getLogger()


def test_oasis_node_info_status(fastapi_app):
    node = load_test_node()
    assert "id" in node
    # status = oasis_node_info_status(node)
    # assert status is not None
    # status = oasis_node_info(node)
    # logger.info(status)
    status = oasis_node_status(node)
    logger.info(status)
    node = load_test_node()
    status = oasis_node_status(node)
    logger.info(status)
