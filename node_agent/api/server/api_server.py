#!/usr/bin/3
from flask import request, Blueprint

from node_agent.api.api_key import require_appkey
from node_agent.model.entrypoint import Entrypoint
from node_agent.model.server import Server
from node_agent.utils.db_util import \
    inset_or_update_object_from_json, \
    delete_object, \
    get_object_list

server_api = Blueprint('server_api', __name__)


@server_api.route("/api/server", methods=['PUT'])
@require_appkey
def api_server_put():
    """Create or update a Server object
    ---
    put:
        description: Put a new Server or update it
        response:
            200:
                content:
                    application/json:
                        schema: Server

    """
    return inset_or_update_object_from_json(Server, request.json)


@server_api.route("/api/server/entrypoint", methods=['PUT'])
@require_appkey
def api_entrypoint_put():
    return inset_or_update_object_from_json(Entrypoint, request.json)


@server_api.route("/api/server", methods=['GET'])
@require_appkey
def api_server_get():
    return get_object_list(Server)


@server_api.route("/api/server/entrypoint", methods=['GET'])
@require_appkey
def api_entrypoint_get():
    return get_object_list(Entrypoint)


@server_api.route("/api/server/<server_id>", methods=['DELETE'])
@require_appkey
def api_server_delete(server_id):
    return delete_object(Server, server_id)


@server_api.route("/api/server/entrypoint/<entrypoint_id>", methods=['DELETE'])
@require_appkey
def api_entrypoint_delete(entrypoint_id):
    return delete_object(Entrypoint, entrypoint_id)
