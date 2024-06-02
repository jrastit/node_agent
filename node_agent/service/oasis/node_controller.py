import logging
from node_agent.shell.shell import execute_remote_command_to_json

logger = logging.getLogger()


def oasis_node_get_json_info_from_command(
    command,
    oasis_node,
):
    remote_node_path = oasis_node["entrypoint"]["path"]
    if remote_node_path is None:
        raise Exception("Remote node entrypoint/path is not defined")
    if oasis_node["core_version"] is None:
        raise Exception("Oasis node core_version is not defined")
    oasis_version = oasis_node["core_version"]
    cmd = [
        remote_node_path
        + "/oasis-core/oasis_core_"
        + oasis_version
        + "_linux_amd64/oasis-node",
        "-a",
        "unix:" + remote_node_path + "/node/data/internal.sock",
    ]
    cmd.extend(command)
    user = oasis_node["entrypoint"]["user"]
    if user is None:
        raise Exception("Remote node entrypoint/user is not defined")
    ip = oasis_node["entrypoint"]["server"]["ip"]
    if ip is None:
        raise Exception("Remote node entrypoint/server/ip is not defined")
    status = execute_remote_command_to_json(cmd, remote_node_path, user, ip)
    return status
