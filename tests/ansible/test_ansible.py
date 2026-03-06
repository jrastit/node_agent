import logging
from node_agent.config import settings
from node_agent.ansible.ansible_run import ansible_run
from node_agent.ansible.server.status import retrieve_server_state
import json

logger = logging.getLogger(__name__)


def test_ansible():
    ansible_run()


def test_ansible_server():
    ret = retrieve_server_state(
        hosts=["localhost", settings.ansible_test_host]
    )
    logger.info("Server state: %s", json.dumps(ret, indent=2))
