#!/usr/bin/3
from flask import jsonify, request, Blueprint

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
from node_agent.utils.db_util import (
    inset_or_update_object_from_json,
    delete_object,
    get_object_list,
    inset_or_update_object_from_json_raw,
)

oasis_api = Blueprint("oasis_api", __name__)


@oasis_api.route("/api/oasis/node", methods=["PUT"])
@require_appkey
def api_oasis_node_put():
    ret = inset_or_update_object_from_json_raw(OasisNode, request.json)
    oasis_node_data_update_nodetype(ret, request.json)
    return jsonify({OasisNode.__name__: ret.to_dict() if ret else None})


@oasis_api.route("/api/oasis/nodetype", methods=["PUT"])
@require_appkey
def api_oasis_nodetype_put():
    return inset_or_update_object_from_json(OasisNodetype, request.json)


@oasis_api.route("/api/oasis/network", methods=["PUT"])
@require_appkey
def api_oasis_network_put():
    return inset_or_update_object_from_json(OasisNetwork, request.json)


@oasis_api.route("/api/oasis/entity", methods=["PUT"])
@require_appkey
def api_oasis_entity_put():
    return inset_or_update_object_from_json(OasisEntity, request.json)


@oasis_api.route("/api/oasis/node", methods=["GET"])
@require_appkey
def api_oasis_node_get():
    return get_object_list(OasisNode)


@oasis_api.route("/api/oasis/nodetype", methods=["GET"])
@require_appkey
def api_nodetype_get():
    return get_object_list(OasisNodetype)


@oasis_api.route("/api/oasis/network", methods=["GET"])
@require_appkey
def api_network_get():
    return get_object_list(OasisNetwork)


@oasis_api.route("/api/oasis/entity", methods=["GET"])
@require_appkey
def api_oasis_entity_get():
    return get_object_list(OasisEntity)


@oasis_api.route("/api/oasis/node/<node_id>", methods=["DELETE"])
@require_appkey
def api_oasis_node_delete(node_id):
    return delete_object(OasisNode, node_id)


@oasis_api.route("/api/oasis/nodetype/<nodetype_id>", methods=["DELETE"])
@require_appkey
def api_nodetype_delete(nodetype_id):
    return delete_object(OasisNodetype, nodetype_id)


@oasis_api.route("/api/oasis/network/<network_id>", methods=["DELETE"])
@require_appkey
def api_network_delete(network_id):
    return delete_object(OasisNetwork, network_id)


@oasis_api.route("/api/oasis/entity/<entity_id>", methods=["DELETE"])
@require_appkey
def api_entity_delete(entity_id):
    return delete_object(OasisEntity, entity_id)


@oasis_api.route("/api/oasis/config/save", methods=["PUT"])
@require_appkey
def api_oasis_config_save():
    if False:
        current_datetime = datetime.datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )
        return export_oasis_config(
            f"export/oasis_config_{current_datetime}.json"
        )
    return export_oasis_config(f"export/oasis_config_test.json")
