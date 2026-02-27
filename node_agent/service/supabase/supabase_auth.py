import logging
import supabase

from node_agent.config import settings
from node_agent.data.user_data import get_user_from_supabase
from node_agent.service.supabase.supabase_client import supabase_client

logger = logging.getLogger(__name__)


def supabase_get_user_from_email(email: str) -> dict:
    client = supabase_client()
    users = client.auth.admin.list_users()
    users = [user for user in users if user.email == email]
    if len(users) == 0:
        logger.warning(f"No user found with email: {email}")
        return None
    return get_user_from_supabase(users[0])


def supabase_auth_with_token(token: str) -> dict:
    client = supabase_client()
    try:
        response = client.auth.get_user(token)
        supabase_user = response.user
        return get_user_from_supabase(supabase_user)
    except Exception as e:
        logger.error(f"Authentication failed: {e}", exc_info=True)
        return None


def supabase_register_user(email: str, password: str) -> dict:
    client = supabase_client()
    try:
        response = client.auth.admin.create_user(
            {"email": email, "password": password, "email_confirm": True}
        )
        if response.user is None:
            raise Exception("User registration failed, no user returned")
        supabase_user = response.user
        user = get_user_from_supabase(supabase_user)
        return user
    except Exception as e:
        logger.error(f"User registration failed: {e}", exc_info=True)
        return None


def supabase_auth_with_password(email: str, password: str) -> tuple:
    client = supabase_client()
    try:
        try:
            response = client.auth.sign_in_with_password(
                {"email": email, "password": password}
            )
        except TypeError:
            response = client.auth.sign_in_with_password(
                email=email, password=password
            )
        if response.user is None:
            logger.warning(f"Authentication failed for email: {email}")
            return None, None
        supabase_user = response.user
        session = response.session
        return session, get_user_from_supabase(supabase_user)
    except Exception as e:
        logger.error(f"Authentication failed: {e}", exc_info=True)
        return None, None
