import logging

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
    session2, user3 = user_util_get_test_user(random=True)
    assert session2 is not None
    assert user3 is not None
    assert user3["id"] is not None
    assert user3["id"] != user["id"]
    assert user3["auth_user_id"] != user["auth_user_id"]
