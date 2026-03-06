import logging

from node_agent.data.server_data import (
    server_data_get_server,
    server_ssh_data_create_full,
)
from node_agent.config import settings
from node_agent.data.server_status_data import server_status_data_get_lastest
from node_agent.service.server.server_status import (
    server_status_update_dynamic,
    server_status_update_static,
)
from tests.utils.user_util import user_util_get_test_organization

logger = logging.getLogger(__name__)


def test_server_status_update():
    organization = user_util_get_test_organization(random=False)[2]
    organization_id = organization["id"]
    ansible_test_host = settings.ansible_test_host
    host = ansible_test_host.split("@")[1]
    port = 22
    user = ansible_test_host.split("@")[0]
    ret_1 = server_ssh_data_create_full(
        server_name="test_server",
        organization_id=organization_id,
        host_name=host,
        port=port,
        ssh_user_name=user,
    )
    server_id_1 = ret_1["server"]["id"]
    ret_2 = server_ssh_data_create_full(
        server_name="test_server_2",
        organization_id=organization_id,
        host_name="localhost",
        port=port,
        ssh_user_name=user,
    )
    server_id_2 = ret_2["server"]["id"]
    server_status_update_static(organization_id)
    server_1 = server_data_get_server(server_id_1)
    logger.info(server_1)
    assert server_1 is not None
    assert server_1["ip"] is not None
    assert server_1["hostname"] is not None
    assert server_1["fqdn"] is not None
    server_2 = server_data_get_server(server_id_2)
    logger.info(server_2)
    assert server_2 is not None
    assert server_2["ip"] is not None
    assert server_2["hostname"] is not None
    assert server_2["fqdn"] is not None
    server_status_update_dynamic(organization_id)
    status_1 = server_status_data_get_lastest(server_id_1)
    logger.info(status_1)
