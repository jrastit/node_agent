#!/usr/bin/3
from fastapi import APIRouter, Depends

from node_agent.api.api_key import require_appkey
from node_agent.model.entrypoint import Entrypoint
from node_agent.model.server import Server
from node_agent.utils.db_util import (
    inset_or_update_object_from_json,
    delete_object,
    get_object_list,
)

server_api = APIRouter()


@server_api.put("/api/server", dependencies=[Depends(require_appkey)])
def api_server_put(payload: dict):
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
    return inset_or_update_object_from_json(Server, payload)


@server_api.put(
    "/api/server/entrypoint", dependencies=[Depends(require_appkey)]
)
def api_entrypoint_put(payload: dict):
    return inset_or_update_object_from_json(Entrypoint, payload)


@server_api.get("/api/server", dependencies=[Depends(require_appkey)])
def api_server_get():
    return get_object_list(Server)


@server_api.get(
    "/api/server/entrypoint", dependencies=[Depends(require_appkey)]
)
def api_entrypoint_get():
    return get_object_list(Entrypoint)


@server_api.delete(
    "/api/server/{server_id}", dependencies=[Depends(require_appkey)]
)
def api_server_delete(server_id: int):
    return delete_object(Server, server_id)


@server_api.delete(
    "/api/server/entrypoint/{entrypoint_id}",
    dependencies=[Depends(require_appkey)],
)
def api_entrypoint_delete(entrypoint_id: int):
    return delete_object(Entrypoint, entrypoint_id)
