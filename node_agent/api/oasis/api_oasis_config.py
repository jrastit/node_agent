#!/usr/bin/3
from flask import jsonify, request, Blueprint

from node_agent.api.api_key import require_appkey
from node_agent.model.oasis.config import OasisParatimeConfig, OasisConfig

from node_agent.utils.db_util import (
    delete_object,
    get_object_list,
    inset_or_update_object_from_json_raw,
)

oasis_config = Blueprint("oasis_config", __name__)


@oasis_config.route("/api/oasis/config", methods=["PUT"])
@require_appkey
def api_oasis_config_put():
    ret = inset_or_update_object_from_json_raw(OasisConfig, request.json)
    return jsonify({OasisConfig.__name__: ret})


@oasis_config.route("/api/oasis/config/<config_id>/paratime", methods=["PUT"])
@require_appkey
def api_oasis_paratime_config_put(config_id):
    ret = inset_or_update_object_from_json_raw(
        OasisParatimeConfig, request.json
    )
    return jsonify({OasisParatimeConfig.__name__: ret})


@oasis_config.route("/api/oasis/config", methods=["GET"])
@require_appkey
def api_oasis_config_get():
    return get_object_list(OasisConfig)


@oasis_config.route("/api/oasis/config/<config_id>/validate", methods=["POST"])
@require_appkey
def api_oasis_config_validate(config_id):
    validate = request.json.get("validate")
    oasis_config = OasisConfig.query.get(config_id)
    oasis_config.validate = validate
    oasis_config.save()
    return jsonify({OasisConfig.__name__: (oasis_config)})


@oasis_config.route("/api/oasis/config/<config_id>", methods=["DELETE"])
@require_appkey
def api_oasis_config_delete(config_id):
    return delete_object(OasisConfig, config_id)
