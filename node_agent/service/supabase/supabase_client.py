from supabase import create_client, Client
from supabase_auth import Session

from node_agent.config import settings


def supabase_client() -> Client:

    url: str = settings.supabase_url
    key: str = settings.supabase_key
    return create_client(url, key)


def supabase_public_client() -> Client:
    url: str = settings.supabase_url
    key: str = settings.supabase_public_key
    return create_client(url, key)


def supabase_client_from_session(session: Session) -> Client:
    client = supabase_public_client()
    client.auth.set_session(
        session.access_token,
        session.refresh_token,
    )
    return client
