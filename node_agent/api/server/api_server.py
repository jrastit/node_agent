#!/usr/bin/3
from fastapi import APIRouter, Depends

from node_agent.api.api_key import require_appkey
from node_agent.model.entrypoint import Entrypoint
from node_agent.model.server import Server
from node_agent.schema.api_schema import (
    EntrypointUpsertSchema,
    ServerUpsertSchema,
)
from node_agent.utils.db_util import (
    inset_or_update_object_from_json,
    delete_object,
    get_object_list,
)
from node_agent.api.server.server_host import server_host_api
from node_agent.api.server.server_port import server_port_api
from node_agent.api.server.server_ssh import server_ssh_api

server_api = APIRouter()
server_api.include_router(server_host_api)
server_api.include_router(server_port_api)
server_api.include_router(server_ssh_api)


@server_api.put("/api/server", dependencies=[Depends(require_appkey)])
def api_server_put(payload: ServerUpsertSchema):
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
    return inset_or_update_object_from_json(
        Server,
        payload.model_dump(exclude_none=True),
    )


@server_api.put(
    "/api/server/entrypoint", dependencies=[Depends(require_appkey)]
)
def api_entrypoint_put(payload: EntrypointUpsertSchema):
    return inset_or_update_object_from_json(
        Entrypoint,
        payload.model_dump(exclude_none=True),
    )


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
