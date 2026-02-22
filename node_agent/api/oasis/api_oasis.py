#!/usr/bin/3
from fastapi import APIRouter, Depends

from node_agent.api.api_key import require_appkey
from node_agent.data.oasis.oasis_node_data import (
    oasis_node_data_update_nodetype,
)
from node_agent.model.oasis.nodetype import OasisNodetype
from node_agent.model.oasis.node import OasisNode
from node_agent.model.oasis.network import OasisNetwork
from node_agent.model.oasis.entity import OasisEntity


from node_agent.service.oasis.oasis_config import export_oasis_config
import datetime
from node_agent.schema.api_schema import (
    OasisNodeUpsertSchema,
    OasisNodetypeUpsertSchema,
    OasisNetworkUpsertSchema,
    OasisEntityUpsertSchema,
)
from node_agent.utils.db_util import (
    inset_or_update_object_from_json,
    delete_object,
    get_object_list,
    inset_or_update_object_from_json_raw,
    _serialize_model,
)

oasis_api = APIRouter()


@oasis_api.put("/api/oasis/node", dependencies=[Depends(require_appkey)])
def api_oasis_node_put(payload: OasisNodeUpsertSchema):
    payload_data = payload.model_dump(exclude_none=True)
    nodetype_ids = payload_data.pop("nodetype_id", None)

    ret = inset_or_update_object_from_json_raw(OasisNode, payload_data)
    if nodetype_ids is not None:
        payload_data["nodetype_id"] = nodetype_ids
    oasis_node_data_update_nodetype(ret, payload_data)
    return {OasisNode.__name__: _serialize_model(ret)}


@oasis_api.put("/api/oasis/nodetype", dependencies=[Depends(require_appkey)])
def api_oasis_nodetype_put(payload: OasisNodetypeUpsertSchema):
    return inset_or_update_object_from_json(
        OasisNodetype,
        payload.model_dump(exclude_none=True),
    )


@oasis_api.put("/api/oasis/network", dependencies=[Depends(require_appkey)])
def api_oasis_network_put(payload: OasisNetworkUpsertSchema):
    return inset_or_update_object_from_json(
        OasisNetwork,
        payload.model_dump(exclude_none=True),
    )


@oasis_api.put("/api/oasis/entity", dependencies=[Depends(require_appkey)])
def api_oasis_entity_put(payload: OasisEntityUpsertSchema):
    return inset_or_update_object_from_json(
        OasisEntity,
        payload.model_dump(exclude_none=True),
    )


@oasis_api.get("/api/oasis/node", dependencies=[Depends(require_appkey)])
def api_oasis_node_get():
    return get_object_list(OasisNode)


@oasis_api.get("/api/oasis/nodetype", dependencies=[Depends(require_appkey)])
def api_nodetype_get():
    return get_object_list(OasisNodetype)


@oasis_api.get("/api/oasis/network", dependencies=[Depends(require_appkey)])
def api_network_get():
    return get_object_list(OasisNetwork)


@oasis_api.get("/api/oasis/entity", dependencies=[Depends(require_appkey)])
def api_oasis_entity_get():
    return get_object_list(OasisEntity)


@oasis_api.delete(
    "/api/oasis/node/{node_id}", dependencies=[Depends(require_appkey)]
)
def api_oasis_node_delete(node_id: int):
    return delete_object(OasisNode, node_id)


@oasis_api.delete(
    "/api/oasis/nodetype/{nodetype_id}",
    dependencies=[Depends(require_appkey)],
)
def api_nodetype_delete(nodetype_id: int):
    return delete_object(OasisNodetype, nodetype_id)


@oasis_api.delete(
    "/api/oasis/network/{network_id}", dependencies=[Depends(require_appkey)]
)
def api_network_delete(network_id: int):
    return delete_object(OasisNetwork, network_id)


@oasis_api.delete(
    "/api/oasis/entity/{entity_id}", dependencies=[Depends(require_appkey)]
)
def api_entity_delete(entity_id: int):
    return delete_object(OasisEntity, entity_id)


@oasis_api.put(
    "/api/oasis/config/save", dependencies=[Depends(require_appkey)]
)
def api_oasis_config_save():
    if False:
        current_datetime = datetime.datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )
        return export_oasis_config(
            f"export/oasis_config_{current_datetime}.json"
        )
    return export_oasis_config(f"export/oasis_config_test.json")
