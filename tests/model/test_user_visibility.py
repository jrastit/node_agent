import logging

from tests.utils.user_util import user_util_get_test_supabase_client

logger = logging.getLogger(__name__)


def test_user_visibility():
    # admin_client = supabase_client()
    # response = admin_client.from_("user").select("*").execute()
    # assert response is not None, "No response from user table query"
    # assert (
    #     response.data is not None
    # ), "No data in response from user table query"
    # assert isinstance(
    #     response.data, list
    # ), "Response data is not a list from user table query"
    # assert len(response.data) > 0, "No user found in user table query"
    # for user in response.data:
    #     assert "id" in user, "User ID not found in user table query result"
    #     assert (
    #         "email" in user
    #     ), "User email not found in user table query result"
    test_client, _session, _user = user_util_get_test_supabase_client()
    response_public = test_client.from_("user").select("*").execute()
    assert (
        response_public is not None
    ), "No response from user table query with public client - this should still work"
    assert (
        response_public.data is not None
    ), "No data in response from user table query with public client - this should still work"
    assert isinstance(
        response_public.data, list
    ), "Response data is not a list from user table query with public client - this should still work"
    assert (
        len(response_public.data) > 0
    ), "No user found in user table query with public client - this should still work"
    for user in response_public.data:
        logger.info(f"User from public client query: {user}")
        assert (
            user.get("id") is not None
        ), "User ID not found in user table query result with public client - this should still work"
        assert user.get("id") == _user.get(
            "id"
        ), "User ID from public client query does not match test user ID - this should still work"

    test_client, _session, _user = user_util_get_test_supabase_client(
        random=True
    )
    response_public = test_client.from_("user").select("*").execute()
    assert (
        response_public is not None
    ), "No response from user table query with public client - this should still work"
    assert (
        response_public.data is not None
    ), "No data in response from user table query with public client - this should still work"
    assert isinstance(
        response_public.data, list
    ), "Response data is not a list from user table query with public client - this should still work"
    assert (
        len(response_public.data) == 1
    ), "No user found in user table query with public client - this should still work"
    for user in response_public.data:
        logger.info(f"User from public client query: {user}")
        assert (
            user.get("id") is not None
        ), "User ID not found in user table query result with public client - this should still work"
        assert user.get("id") == _user.get(
            "id"
        ), "User ID from public client query does not match test user ID - this should still work"
