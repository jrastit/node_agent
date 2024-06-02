from datetime import datetime
from datetime import datetime, timezone

from node_agent.oasis.node_controller import (
    oasis_node_get_json_info_from_command,
)


def oasis_node_info_status(oasis_node):
    cmd = ["control", "status"]
    return oasis_node_get_json_info_from_command(cmd, oasis_node)


def oasis_node_info(oasis_node):
    status = oasis_node_info_status(oasis_node)
    core_version = None
    node_id = None
    latest_time = None
    last_registration = None
    is_validator = None
    if "software_version" in status:
        core_version = status["software_version"]
    if "identity" in status:
        if "node" in status["identity"]:
            node_id = status["identity"]["node"]
    if "consensus" in status:
        if "latest_time" in status["consensus"]:
            latest_time = status["consensus"]["latest_time"]
        if "is_validator" in status["consensus"]:
            is_validator = status["consensus"]["is_validator"]
    if "registration" in status:
        if "last_registration" in status["registration"]:
            last_registration = status["registration"]["last_registration"]

    return {
        "core_version": core_version,
        "node_id": node_id,
        "latest_time": latest_time,
        "last_registration": last_registration,
        "is_validator": is_validator,
    }


def oasis_node_status(oasis_node):
    node_info = oasis_node_info(oasis_node)
    if node_info["last_registration"] is not None:
        last_registration_delay = datetime.now(
            timezone.utc
        ) - datetime.fromisoformat(node_info["last_registration"])
    if node_info["latest_time"] is not None:
        latest_time_delay = datetime.now(
            timezone.utc
        ) - datetime.fromisoformat(node_info["latest_time"])
    node_info["last_registration_delay"] = last_registration_delay
    node_info["latest_time_delay"] = latest_time_delay
    return node_info
