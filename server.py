#!/usr/bin/3
from node_agent.utils.thread import set_thread_available

from node_agent.myapp import init_app

set_thread_available(1)

print('Start ' + __name__)

app = init_app()











