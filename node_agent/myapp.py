#!/usr/bin/3

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from node_agent.config import get_database_uri
from node_agent.model.db import db

from node_agent.api.test.api_test import test_api
from node_agent.api.server.api_server import server_api
from node_agent.api.oasis.api_oasis import oasis_api
from node_agent.api.oasis.api_oasis_config import oasis_config
from node_agent.api.organisation.api_organisation import organisation_api


def _init_db():
    db.init(
        get_database_uri(),
        {
            "connect_args": {
                "connect_timeout": 5,
                "options": "-c lock_timeout=3000 -c statement_timeout=3000",
            }
        },
    )


def init_app(init_db=True):
    if init_db:
        _init_db()

    app = FastAPI(title="node_agent", version="1.0.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(test_api)
    app.include_router(server_api)
    app.include_router(oasis_api)
    app.include_router(oasis_config)
    app.include_router(organisation_api)

    @app.get("/api/swagger.json")
    def specs():
        root_path = Path(__file__).resolve().parents[1]
        return FileResponse(str(root_path / "swagger.json"))

    return app
