import logging
from node_agent.shell.shell import execute_remote_command_to_json

logger = logging.getLogger()


def entrypoint_get_json_info_from_command(
    command,
    entrypoint,
):
    remote_node_path = entrypoint["path"]
    if remote_node_path is None:
        raise Exception("Remote node entrypoint/path is not defined")
    user = entrypoint["user"]
    if user is None:
        raise Exception("Remote node entrypoint/user is not defined")
    ip = entrypoint["server"]["ip"]
    if ip is None:
        raise Exception("Remote node entrypoint/server/ip is not defined")
    status = execute_remote_command_to_json(
        command, remote_node_path, user, ip
    )
    return status
