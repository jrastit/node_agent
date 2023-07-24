from node_agent.shell.shell import execute_remote_command_to_json


def oasis_node_get_json_info_from_command(
        command,
        remote_node_path='/oasis/testnet_google',
        oasis_version='22.2.9'
):
    cmd = [
        remote_node_path + "/oasis-core/oasis_core_" + oasis_version + "_linux_amd64/oasis-node",
        "-a", "unix:" + remote_node_path + "/node/data/internal.sock",
    ]
    cmd.extends(command)
    status = execute_remote_command_to_json(cmd)
    print(dict(status))
    print(status['software_version'])









