import logging

from tests.utils.api_util import (
    api_put_data,
    api_simple_get,
    api_simple_delete,
)

logger = logging.getLogger(__name__)


def test_api_organization_post_error(fastapi_app):
    ret = api_put_data("/api/organization", 422, {"error": False})
    assert ret is not None
    assert "detail" in ret


def test_api_organization(fastapi_app):
    organization_handler = api_put_data(
        "/api/organization",
        200,
        {
            "name": "api_test_organization",
        },
    )
    assert "Organization" in organization_handler
    organization = organization_handler["Organization"]
    assert "id" in organization
    organization_id = organization["id"]
    assert "name" in organization
    assert organization["name"] == "api_test_organization"

    organization_handler = api_put_data(
        "/api/organization",
        200,
        {
            "id": organization_id,
            "name": "api_test_organization_v2",
        },
    )
    assert "Organization" in organization_handler
    organization = organization_handler["Organization"]
    assert "id" in organization
    assert organization["id"] == organization_id
    assert "name" in organization
    assert organization["name"] == "api_test_organization_v2"

    organization_list_handler = api_simple_get("/api/organization", 200)
    assert "Organization" in organization_list_handler
    organization_list = organization_list_handler["Organization"]
    found = False
    for _organization in organization_list:
        logger.info("Organization: %s", _organization)
        if _organization["id"] == organization_id:
            assert "name" in _organization
            assert _organization["name"] == "api_test_organization_v2"
            found = True
    assert found is True

    ret = api_simple_delete("/api/organization/" + str(organization_id), 200)
    assert "Status" in ret
    assert ret["Status"] == "success"

    organization_list_handler = api_simple_get("/api/organization", 200)
    assert "Organization" in organization_list_handler
    organization_list = organization_list_handler["Organization"]
    found = False
    for _organization in organization_list:
        if _organization["id"] == organization_id:
            assert "name" in _organization
            assert _organization["name"] == "api_test_organization_v2"
            found = True
    assert found is False
