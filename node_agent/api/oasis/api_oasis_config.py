#!/usr/bin/3
from fastapi import APIRouter, Depends

from node_agent.api.api_key import require_appkey
from node_agent.model.db import db
from node_agent.model.oasis.config import OasisParatimeConfig, OasisConfig

from node_agent.utils.db_util import (
    delete_object,
    get_object_list,
    inset_or_update_object_from_json_raw,
    _serialize_model,
)

oasis_config = APIRouter()


@oasis_config.put("/api/oasis/config", dependencies=[Depends(require_appkey)])
def api_oasis_config_put(payload: dict):
    ret = inset_or_update_object_from_json_raw(OasisConfig, payload)
    return {OasisConfig.__name__: _serialize_model(ret)}


@oasis_config.put(
    "/api/oasis/config/{config_id}/paratime",
    dependencies=[Depends(require_appkey)],
)
def api_oasis_paratime_config_put(config_id: int, payload: dict):
    payload["oasis_config_id"] = config_id
    ret = inset_or_update_object_from_json_raw(OasisParatimeConfig, payload)
    return {OasisParatimeConfig.__name__: _serialize_model(ret)}


@oasis_config.get("/api/oasis/config", dependencies=[Depends(require_appkey)])
def api_oasis_config_get():
    return get_object_list(OasisConfig)


@oasis_config.post(
    "/api/oasis/config/{config_id}/validate",
    dependencies=[Depends(require_appkey)],
)
def api_oasis_config_validate(config_id: int, payload: dict):
    validate = payload.get("validate")
    oasis_config = db.session.get(OasisConfig, config_id)
    oasis_config.validate = validate
    db.session.commit()
    return {OasisConfig.__name__: _serialize_model(oasis_config)}


@oasis_config.delete(
    "/api/oasis/config/{config_id}", dependencies=[Depends(require_appkey)]
)
def api_oasis_config_delete(config_id: int):
    return delete_object(OasisConfig, config_id)
