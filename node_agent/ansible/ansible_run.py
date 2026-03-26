#!/usr/bin/env python
import logging

from node_agent.ansible.ansible_playbook import AnsiblePlaybook

logger = logging.getLogger(__name__)


def ansible_run():
    playbook = AnsiblePlaybook(
        hosts=["localhost"],
        tasks=[
            {
                "action": "ansible.builtin.shell",
                "args": {"cmd": "ls"},
                "register": "shell_out",
            },
            {
                "action": "ansible.builtin.debug",
                "args": {"msg": "{{shell_out.stdout}}"},
            },
            {
                "action": "ansible.builtin.command",
                "args": {"cmd": "/usr/bin/uptime"},
            },
        ],
    )

    output = playbook.play()

    logger.info("UP ***********")
    for host, result in output["ok"].items():
        logger.info("{0} >>> {1}".format(host, result.get("stdout", "")))

    logger.info("FAILED *******")
    for host, result in output["failed"].items():
        logger.info("{0} >>> {1}".format(host, result.get("msg", "")))

    logger.info("DOWN *********")
    for host, result in output["unreachable"].items():
        logger.info("{0} >>> {1}".format(host, result.get("msg", "")))
