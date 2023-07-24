import json
from io import StringIO

import yaml
from apispec import APISpec
from apispec_webframeworks.flask import FlaskPlugin
from dataclasses_jsonschema.apispec import DataclassesPlugin

from node_agent.api.server.api_server import api_server_put
from node_agent.model.db import Base
from node_agent.model.entrypoint import Entrypoint
from node_agent.model.oasis.entity import OasisEntity
from node_agent.model.oasis.network import OasisNetwork
from node_agent.model.oasis.node import OasisNode
from node_agent.model.oasis.nodetype import OasisNodetype
from node_agent.model.server import Server

# Create an APISpec
spec = APISpec(
    title="Node Agent API",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), DataclassesPlugin()],
)


def config_apispec(app):
    with app.test_request_context():
        print(dict(Server.json_schema()))
        spec.components.schema("Base", schema=Base)
        print(dict(spec.to_dict()))
        spec.components.schema("Server", Server.json_schema(), schema=Server)
        print(dict(spec.to_dict()))
        spec.components.schema("Entrypoint", schema=Entrypoint)
        print(dict(spec.to_dict()))
        spec.components.schema("OasisNode", schema=OasisNode)
        spec.components.schema("OasisNodetype", schema=OasisNodetype)
        spec.components.schema("OasisNetwork", schema=OasisNetwork)
        spec.components.schema("OasisEntity", schema=OasisEntity)
        spec.path(view=api_server_put)
        with open('swagger.json', 'w') as f:
            dict_ = yaml.load(StringIO(spec.to_yaml()), Loader=yaml.SafeLoader)
            with open('swagger.json', 'w') as f:
                json.dump(dict_, f)

