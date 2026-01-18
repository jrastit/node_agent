#!/usr/bin/3

from flask import Flask, send_from_directory
from flask_cors import CORS

from node_agent.api.api_swagger import swaggerui_blueprint
from node_agent.config import get_database_uri, settings

from node_agent.global_var import set_app
from node_agent.model.db import db, Base

from node_agent.api.test.api_test import test_api
from node_agent.api.server.api_server import server_api
from node_agent.api.oasis.api_oasis import oasis_api
from node_agent.api.oasis.api_oasis_config import oasis_config


def init_app():
    # Create the web app
    app = Flask(__name__)
    # Added for allow origin issue
    CORS(app)
    # configure the Postgres database
    # app.config['SQLALCHEMY_ECHO'] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = get_database_uri()
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "connect_args": {
            "connect_timeout": 5,
            "options": "-c lock_timeout=3000 -c statement_timeout=3000",
        }
    }
    db.init_app(app)
    app.app_context().push()

    # Register app services per section
    app.register_blueprint(test_api)
    app.register_blueprint(server_api)
    app.register_blueprint(oasis_api)
    app.register_blueprint(oasis_config)
    # Support OpenApi V3
    # app.config["SWAGGER"]['openapi'] = '3.0.2'
    # Base.metadata.create_all(db.engine)
    # db.create_all()
    set_app(app)

    app.register_blueprint(swaggerui_blueprint())

    @app.route("/api/swagger.json")
    def specs():
        return send_from_directory("../", "swagger.json")

    return app
