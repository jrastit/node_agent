import logging

from node_agent.data.organization_data import organization_data_create
from node_agent.data.server_data import server_ssh_data_create_full
from node_agent.service.supabase.supabase_auth import supabase_auth_with_token
from tests.utils.user_util import user_util_get_test_user

logger = logging.getLogger(__name__)


def test_supabase_test_user():

    session, user = user_util_get_test_user()
    assert session is not None
    assert user is not None
    logger.info(
        f"Test user created with ID: {user['id']} and auth_user_id: {user['auth_user_id']}"
    )
    logger.info(f"User details: {user}")
    assert user["id"] is not None
    user2 = supabase_auth_with_token(session.access_token)
    assert user2 is not None
    assert user2["id"] is not None
    assert user2["id"] == user["id"]
    # assert user2["auth_user_id"] == user["auth_user_id"]
    organization = organization_data_create(
        name="test_organization", owner_id=user["id"]
    )
    assert organization is not None
    assert "id" in organization
    assert organization["id"] is not None
    ret = server_ssh_data_create_full(
        server_name="test_server",
        organization_id=organization["id"],
        server_ip="127.0.0.1",
        cloud="test_cloud",
        cloud_name="Test Cloud",
        host_name="127.0.0.1",
        host_description="Test Host",
        port="22",
        port_description="Test Port",
        ssh_user_name="test_user",
        ssh_description="Test SSH",
    )
    assert ret is not None
    assert ret.get("server") is not None
    assert ret.get("server_host") is not None
    assert ret.get("server_port") is not None
    assert ret.get("server_ssh") is not None


def test_supabase_test_user2():

    session, user = user_util_get_test_user()
    assert session is not None
    assert user is not None
