import pytest

from node_agent.model.oasis.entity import OasisEntity
from node_agent.model.oasis.network import OasisNetwork
from node_agent.model.oasis.nodetype import OasisNodetype
from node_agent.myapp import init_app
from node_agent.utils.thread import get_nb_thread, set_thread_available


@pytest.fixture
def app():
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
