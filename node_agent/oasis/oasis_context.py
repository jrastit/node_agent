from node_agent.model.oasis.node import OasisNode
from node_agent.shell.server_context import ServerContext


class OasisContext(ServerContext):
    def __init__(self, node: OasisNode):
        super().__init__(node.entrypoint if node.entrypoint else None)