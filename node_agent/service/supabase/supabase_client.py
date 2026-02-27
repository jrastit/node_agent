from supabase import create_client, Client
from node_agent.config import settings


def supabase_client() -> Client:

    url: str = settings.supabase_url
    key: str = settings.supabase_key
    return create_client(url, key)
