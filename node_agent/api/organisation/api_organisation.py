from fastapi import APIRouter, Depends
from node_agent.api.api_key import require_appkey
from node_agent.model.organisation import Organisation
from node_agent.schema.api_schema import OrganisationUpsertSchema
from node_agent.utils.db_util import (
    inset_or_update_object_from_json,
    delete_object,
    get_object_list,
)

organisation_api = APIRouter()


@organisation_api.put(
    "/api/organisation", dependencies=[Depends(require_appkey)]
)
def api_organisation_put(payload: OrganisationUpsertSchema):
    """Create or update an Organisation object"""
    return inset_or_update_object_from_json(
        Organisation,
        payload.model_dump(exclude_none=True),
    )


@organisation_api.get(
    "/api/organisation", dependencies=[Depends(require_appkey)]
)
def api_organisation_get():
    return get_object_list(Organisation)


@organisation_api.delete(
    "/api/organisation/{organisation_id}",
    dependencies=[Depends(require_appkey)],
)
def api_organisation_delete(organisation_id: int):
    return delete_object(Organisation, organisation_id)
