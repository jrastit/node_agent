import logging

from tests.utils.api_util import (
    api_put_data,
    api_simple_get,
    api_simple_delete,
)

logger = logging.getLogger(__name__)


def test_api_organisation_post_error(fastapi_app):
    ret = api_put_data("/api/organisation", 422, {"error": False})
    assert ret is not None
    assert "detail" in ret


def test_api_organisation(fastapi_app):
    organisation_handler = api_put_data(
        "/api/organisation",
        200,
        {
            "name": "api_test_organisation",
        },
    )
    assert "Organisation" in organisation_handler
    organisation = organisation_handler["Organisation"]
    assert "id" in organisation
    organisation_id = organisation["id"]
    assert "name" in organisation
    assert organisation["name"] == "api_test_organisation"

    organisation_handler = api_put_data(
        "/api/organisation",
        200,
        {
            "id": organisation_id,
            "name": "api_test_organisation_v2",
        },
    )
    assert "Organisation" in organisation_handler
    organisation = organisation_handler["Organisation"]
    assert "id" in organisation
    assert organisation["id"] == organisation_id
    assert "name" in organisation
    assert organisation["name"] == "api_test_organisation_v2"

    organisation_list_handler = api_simple_get("/api/organisation", 200)
    assert "Organisation" in organisation_list_handler
    organisation_list = organisation_list_handler["Organisation"]
    found = False
    for _organisation in organisation_list:
        logger.info("Organisation: %s", _organisation)
        if _organisation["id"] == organisation_id:
            assert "name" in _organisation
            assert _organisation["name"] == "api_test_organisation_v2"
            found = True
    assert found is True

    ret = api_simple_delete("/api/organisation/" + str(organisation_id), 200)
    assert "Status" in ret
    assert ret["Status"] == "success"

    organisation_list_handler = api_simple_get("/api/organisation", 200)
    assert "Organisation" in organisation_list_handler
    organisation_list = organisation_list_handler["Organisation"]
    found = False
    for _organisation in organisation_list:
        if _organisation["id"] == organisation_id:
            assert "name" in _organisation
            assert _organisation["name"] == "api_test_organisation_v2"
            found = True
    assert found is False
