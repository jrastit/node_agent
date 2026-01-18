from flask import request, Blueprint
from node_agent.api.api_key import require_appkey
from node_agent.model.organisation import Organisation
from node_agent.utils.db_util import (
    inset_or_update_object_from_json,
    delete_object,
    get_object_list,
)

organisation_api = Blueprint('organisation_api', __name__)

@organisation_api.route("/api/organisation", methods=['PUT'])
@require_appkey
def api_organisation_put():
    """Create or update an Organisation object"""
    return inset_or_update_object_from_json(Organisation, request.json)

@organisation_api.route("/api/organisation", methods=['GET'])
@require_appkey
def api_organisation_get():
    return get_object_list(Organisation)

@organisation_api.route("/api/organisation/<organisation_id>", methods=['DELETE'])
@require_appkey
def api_organisation_delete(organisation_id):
    return delete_object(Organisation, organisation_id)
