from node_agent.data.organization_data import organization_data_create
from tests.utils.user_util import user_util_get_test_user


def test_organization_data_create():
    session, user = user_util_get_test_user(random=True)
    assert session is not None
    assert user is not None
    organization = organization_data_create(
        name="test_organization", owner_id=user["id"]
    )
    assert organization is not None
    assert "id" in organization
    assert "name" in organization
    assert organization["name"] == "test_organization"
    assert organization["id"] is not None
    organization = organization_data_create(
        name="test_organization", owner_id=user["id"]
    )
    assert organization is not None
    assert "id" in organization
    assert "name" in organization
    assert organization["name"] == "test_organization"
    assert organization["id"] is not None
