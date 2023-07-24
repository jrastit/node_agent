from node_agent.shell.server_context import ServerContext
from node_agent.shell.shell import execute_remote_command


def test_shell_execute_command():
    server_context = ServerContext()
    server_context.execute_command_to_string(['bash', '-c', 'echo $PWD'])

