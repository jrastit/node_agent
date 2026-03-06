import logging
from node_agent.ansible.server.status_dynamic import retrieve_server_dynamic
from node_agent.ansible.server.status_static import retrieve_server_static
from node_agent.data.server_status_data import server_status_data
from node_agent.data.server_data import get_server_ssh, server_data_update

logger = logging.getLogger(__name__)


def server_status_update_static(organization_id: int):

    ssh_list = get_server_ssh(organization_id)
    for server_id, ssh_str in ssh_list.items():
        logger.info(
            f"Updating server status for server_id: {server_id}, ssh_str: {ssh_str}"
        )
        ansible_result = retrieve_server_static([ssh_str])
        logger.info(
            f"Ansible result for server_id: {server_id}: {ansible_result}"
        )
        hosts = ansible_result.get("hosts", [])
        if not hosts:
            logger.warning(
                "No hosts found in ansible result for server_id=%s", server_id
            )
            continue

        static_fields = hosts[0].get("static_fields", {})
        server_data_update(server_id, static_fields)


def server_status_update_dynamic(organization_id: int):

    ssh_list = get_server_ssh(organization_id)
    for server_id, ssh_str in ssh_list.items():
        logger.info(
            f"Updating server status for server_id: {server_id}, ssh_str: {ssh_str}"
        )
        ansible_result = retrieve_server_dynamic([ssh_str])
        logger.info(
            f"Ansible result for server_id: {server_id}: {ansible_result}"
        )
        hosts = ansible_result.get("hosts", [])
        if not hosts:
            logger.warning(
                "No hosts found in ansible result for server_id=%s", server_id
            )
            continue

        dynamic_fields = hosts[0].get("dynamic_fields", {})
        server_status_data(server_id, dynamic_fields)
