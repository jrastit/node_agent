#!/usr/bin/3
from flask import jsonify, Blueprint


from node_agent.api.api_key import require_appkey

test_api = Blueprint('test_api', __name__)


@test_api.route(
    "/api/test/ping",
    methods=['GET']
)
@require_appkey
def api_test_ping():
    return "Pong"
