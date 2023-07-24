from tests.utils.api_util import \
    api_simple_get


def test_api_test_ping():
    ret = api_simple_get(
        '/api/test/ping',
        200
    )
    assert ret is None
