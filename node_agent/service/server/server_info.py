from node_agent.service.server.server_controller import (
    entrypoint_get_json_info_from_command,
)


def server_get_public_address(entrypoint):
    cmd = ["curl", "'https://api.ipify.org?format=json'"]
    try:
        ret = entrypoint_get_json_info_from_command(cmd, entrypoint)
        return ret
    except Exception as e:
        return {"error": str(e)}
