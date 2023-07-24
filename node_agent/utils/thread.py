from threading import Thread
from node_agent.global_var import get_app

nb_thread = 0

thread_available = 0


def _with_thread(function, *args):
    global nb_thread
    # print('start thread')
    nb_thread = nb_thread + 1
    try:
        with get_app().app_context():
            function(*args)
    except Exception as thread_exception:  # pragma no cover
        print(thread_exception)
        nb_thread = nb_thread - 1
        print('thread exception')
        raise
    nb_thread = nb_thread - 1
    # print('stop thread')


def with_thread(function, *args):
    global thread_available
    if not thread_available:
        raise Exception('Thread are not available')
    Thread(target=_with_thread, args=(function, *args,)).start()


def get_nb_thread():
    global nb_thread
    return nb_thread


def set_thread_available(available):
    global thread_available
    thread_available = available
