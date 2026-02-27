# import sys

# # Monkey-patch dataclasses._asdict_inner pour loguer chaque appel
# _original_asdict_inner = sys.modules["dataclasses"]._asdict_inner
# def debug_asdict_inner(obj, dict_factory):
#     print(f"dataclasses._asdict_inner called on instance of: {type(obj).__name__}")
#     return _original_asdict_inner(obj, dict_factory)
# sys.modules["dataclasses"]._asdict_inner = debug_asdict_inner
# import dataclasses

# _original_asdict = dataclasses.asdict


# def debug_asdict(obj, *, dict_factory=dict):
#     print(f"dataclasses.asdict called on instance of: {type(obj).__name__}")
#     return _original_asdict(obj, dict_factory=dict_factory)


# dataclasses.asdict = debug_asdict
import pytest

from node_agent.model.oasis.entity import OasisEntity
from node_agent.model.oasis.network import OasisNetwork
from node_agent.model.oasis.nodetype import OasisNodetype
from node_agent.myapp import init_app
from node_agent.utils.thread import get_nb_thread, set_thread_available
from tests.utils.user_util import user_util_cleanup_test_user


def pytest_sessionstart(session):
    init_app()
    user_util_cleanup_test_user()


@pytest.fixture
def fastapi_app():
    app = init_app()
    OasisEntity
    OasisNodetype
    OasisNetwork
    return app


@pytest.fixture()
def thread_check():

    set_thread_available(1)

    """Fixture to execute asserts before and after a test is run"""
    # Setup: fill with any logic you want
    assert get_nb_thread() == 0

    yield  # this is where the testing happens

    assert get_nb_thread() == 0

    set_thread_available(0)

    # Teardown : fill with any logic you want
