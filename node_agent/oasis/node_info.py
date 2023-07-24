from node_agent.oasis.node_controller import \
    oasis_node_get_json_info_from_command


def oasis_node_info_status():
    cmd = ["control", "status"]
    return oasis_node_get_json_info_from_command(cmd)
