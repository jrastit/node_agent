from fastapi import APIRouter, Depends
from node_agent.api.api_key import require_appkey
from node_agent.model.organization import Organization
from node_agent.schema.api_schema import OrganizationUpsertSchema
from node_agent.utils.db_util import (
    inset_or_update_object_from_json,
    delete_object,
    get_object_list,
)

organization_api = APIRouter()


@organization_api.put(
    "/api/organization", dependencies=[Depends(require_appkey)]
)
def api_organization_put(payload: OrganizationUpsertSchema):
    """Create or update an Organization object"""
    return inset_or_update_object_from_json(
        Organization,
        payload.model_dump(exclude_none=True),
    )


@organization_api.get(
    "/api/organization", dependencies=[Depends(require_appkey)]
)
def api_organization_get():
    return get_object_list(Organization)


@organization_api.delete(
    "/api/organization/{organization_id}",
    dependencies=[Depends(require_appkey)],
)
def api_organization_delete(organization_id: int):
    return delete_object(Organization, organization_id)
