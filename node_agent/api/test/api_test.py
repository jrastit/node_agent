#!/usr/bin/3
from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse


from node_agent.api.api_key import require_appkey

test_api = APIRouter()


@test_api.get("/api/test/ping", dependencies=[Depends(require_appkey)])
def api_test_ping():
    return PlainTextResponse("Pong")
