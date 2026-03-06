from fastapi import APIRouter, Depends

from node_agent.api.api_key import require_appkey
from node_agent.model.server_port import ServerPort
from node_agent.schema.api_schema import ServerIpUpsertSchema
from node_agent.utils.db_util import (
    inset_or_update_object_from_json,
    delete_object,
    get_object_list,
)

server_port_api = APIRouter()


@server_port_api.put(
    "/api/server/port", dependencies=[Depends(require_appkey)]
)
def api_server_port_put(payload: ServerIpUpsertSchema):
    return inset_or_update_object_from_json(
        ServerPort,
        payload.model_dump(exclude_none=True),
    )


@server_port_api.get(
    "/api/server/port", dependencies=[Depends(require_appkey)]
)
def api_server_port_get():
    return get_object_list(ServerPort)


@server_port_api.delete(
    "/api/server/port/{server_port_id}",
    dependencies=[Depends(require_appkey)],
)
def api_server_port_delete(server_port_id: int):
    return delete_object(ServerPort, server_port_id)
