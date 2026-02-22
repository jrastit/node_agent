from typing import Annotated

from fastapi import Header, HTTPException

from node_agent.config import settings


def _get_api_token() -> str | None:
    token = settings.get("NODE_AGENT_API_TOKEN")
    if token is None:
        token = settings.get("node_agent_api_token")
    if token is None:
        token = "test"
    return token


def require_appkey(
    grpc_metadata_authorization: Annotated[
        str | None, Header(alias="Grpc-Metadata-Authorization")
    ] = None,
):
    token = _get_api_token()
    if grpc_metadata_authorization is None:
        print("Error : no token set")
        raise HTTPException(status_code=401, detail="Unauthorized")
    if grpc_metadata_authorization != f"Bearer {token}":
        print("Error : invalid token")
        raise HTTPException(status_code=401, detail="Unauthorized")
