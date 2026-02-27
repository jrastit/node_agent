import uuid
import logging

from node_agent.config import settings
from node_agent.service.supabase.supabase_auth import (
    supabase_auth_with_password,
    supabase_register_user,
    supabase_get_user_from_email,
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
