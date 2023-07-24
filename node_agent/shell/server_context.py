from node_agent.model.entrypoint import Entrypoint
from node_agent.shell.shell import execute_command, execute_remote_command
import json


class ServerContext:
    def __init__(self, entrypoint=None):
        self.entrypoint = entrypoint

    entrypoint: Entrypoint = None

    def execute_command_to_json(self, cmd):
        out = self.execute_command_to_string(
            cmd,
        )
        return json.loads(out)

    def execute_command_to_string(self, cmd):
        result = self.execute_command(
            cmd,
        )
        return result.stdout

    def execute_command(self, cmd):
        if self.entrypoint \
                and self.entrypoint.server \
                and self.entrypoint.server.ip \
                and self.entrypoint.user:
            return execute_remote_command(
                cmd,
                ip=self.entrypoint.server.ip,
                user=self.entrypoint.user
            )
        return execute_command(cmd)
