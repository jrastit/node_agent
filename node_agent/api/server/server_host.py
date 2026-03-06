from fastapi import APIRouter, Depends

from node_agent.api.api_key import require_appkey
from node_agent.model.server_host import ServerHost
from node_agent.schema.api_schema import ServerHostUpsertSchema
from node_agent.utils.db_util import (
    inset_or_update_object_from_json,
    delete_object,
    get_object_list,
)

server_host_api = APIRouter()


@server_host_api.put(
    "/api/server/host", dependencies=[Depends(require_appkey)]
)
def api_server_host_put(payload: ServerHostUpsertSchema):
    return inset_or_update_object_from_json(
        ServerHost,
        payload.model_dump(exclude_none=True),
    )


@server_host_api.get(
    "/api/server/host", dependencies=[Depends(require_appkey)]
)
def api_server_host_get():
    return get_object_list(ServerHost)


@server_host_api.delete(
    "/api/server/host/{server_host_id}",
    dependencies=[Depends(require_appkey)],
)
def api_server_host_delete(server_host_id: int):
    return delete_object(ServerHost, server_host_id)
