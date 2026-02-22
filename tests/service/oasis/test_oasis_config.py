from tests.utils.test_node import load_test_node


def test_oasis_config(fastapi_app):
    node = load_test_node()
    assert "id" in node
