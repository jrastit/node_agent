import pytest
from node_agent.utils.thread import with_thread


def empty_func():
    return


def test_with_thread():
    with pytest.raises(Exception) as exec_info:
        with_thread(None, None)
    assert str(exec_info.value) == 'Thread are not available'


def test_with_thread2(thread_check):
    with_thread(empty_func)
