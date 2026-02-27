import uuid
import logging

from supabase import Client
from supabase_auth import Session

from node_agent.config import settings
from node_agent.data.organisation_data import organisation_data_create
from node_agent.service.supabase.supabase_auth import (
    supabase_auth_with_password,
    supabase_auth_with_token,
    supabase_get_user_list_from_email,
    supabase_register_user,
    supabase_get_user_from_email,
    supabase_delete_user,
)
from node_agent.service.supabase.supabase_client import (
    supabase_client,
    supabase_client_from_session,
)

logger = logging.getLogger(__name__)

test_user_session = None
test_user = None


def user_util_get_test_user(random=False):
    global test_user_session, test_user
    user_session = None
    user = None
    if test_user is None or test_user_session is None or random:
        if random:
            user_email = f"test_user_{uuid.uuid4()}@example.com"
            user_password = f"{uuid.uuid4()}"
            logger.info(f"Creating random test user with email: {user_email}")
        else:
            user_email = settings.test_user_email
            user_password = settings.test_user_password
        user = supabase_get_user_from_email(user_email)
        if user is None:
            logger.info(
                f"Test user not found with email: {user_email}, creating new user"
            )
            user = supabase_register_user(user_email, user_password)
            assert user is not None, "Test user registration failed"
        if user is not None:
            user_session, user = supabase_auth_with_password(
                user_email, user_password
            )
            assert (
                user_session is not None
            ), "Test user authentication failed after registration"
            assert (
                user is not None
            ), "Test user authentication failed after registration"

    if random:
        return user_session, user
    test_user_session = user_session
    test_user = user

    return test_user_session, test_user


def user_util_get_test_organisation(random=False):
    organisation_name = "test_organisation"
    if random:
        organisation_name += f"_{uuid.uuid4()}"
    session, user = user_util_get_test_user(random=random)
    organisation = organisation_data_create(
        name=organisation_name, owner_id=user["id"]
    )
    return session, user, organisation


def user_util_cleanup_test_user():
    try:
        users = supabase_get_user_list_from_email("test_user_", "@example.com")
        for u in users:
            supabase_delete_user(u)
            logger.info(f"Deleted test user with email: {u['auth_user_id']}")
    except Exception as e:
        logger.error(
            f"Failed to delete test user : {e}",
            exc_info=True,
        )


def user_util_get_test_supabase_client(
    random=False,
) -> tuple[Client, Session, dict]:
    session, user = user_util_get_test_user(random=random)
    assert session is not None, "Failed to get session for test user"
    assert user is not None, "Failed to get user for test user"
    client = supabase_client_from_session(session)
    supabase_user_response = client.auth.get_user()
    assert (
        supabase_user_response is not None
    ), "Failed to get supabase user from session"
    supabase_id_norm = str(
        uuid.UUID(str(supabase_user_response.user.id).strip())
    )
    auth_id_norm = str(uuid.UUID(str(user["auth_user_id"]).strip()))

    assert (
        supabase_id_norm == auth_id_norm
    ), f"Supabase user ID {supabase_id_norm} does not match test user auth_user_id {auth_id_norm}"
    return client, session, user
