from node_agent.model.server import Server
from tests.utils.user_util import user_util_get_test_organization


def test_model_server(fastapi_app):
    organization = user_util_get_test_organization()[2]
    organization_id = organization["id"]
    assert organization_id is not None
    server = Server(organization_id=organization_id)
    assert server is not None
