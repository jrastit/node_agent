from fastapi import APIRouter, Depends

from node_agent.api.api_key import require_appkey
from node_agent.model.server_ssh import ServerSSH
from node_agent.schema.api_schema import ServerSSHUpsertSchema
from node_agent.utils.db_util import (
    inset_or_update_object_from_json,
    delete_object,
    get_object_list,
)

server_ssh_api = APIRouter()


@server_ssh_api.put("/api/server/ssh", dependencies=[Depends(require_appkey)])
def api_server_ssh_put(payload: ServerSSHUpsertSchema):
    return inset_or_update_object_from_json(
        ServerSSH,
        payload.model_dump(exclude_none=True),
    )


@server_ssh_api.get("/api/server/ssh", dependencies=[Depends(require_appkey)])
def api_server_ssh_get():
    return get_object_list(ServerSSH)


@server_ssh_api.delete(
    "/api/server/ssh/{server_ssh_id}",
    dependencies=[Depends(require_appkey)],
)
def api_server_ssh_delete(server_ssh_id: int):
    return delete_object(ServerSSH, server_ssh_id)
