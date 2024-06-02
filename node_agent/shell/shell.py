from __future__ import absolute_import, division, print_function

import logging
import subprocess
import json

import shutil

import ansible.constants as C
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.module_utils.common.collections import ImmutableDict
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.vars.manager import VariableManager
from ansible import context

from node_agent.ansible.results_collector_JSON_callback import (
    ResultsCollectorJSONCallback,
)

logger = logging.getLogger()

# ssh -4 -o StrictHostKeyChecking=accept-new -o ConnectTimeout=10 oasis@217.160.36.2
# /home/oasis/mainnet/oasis-core/oasis_core_22.2.7_linux_amd64/oasis-node -a unix:/home/oasis/mainnet/node/data/internal.sock
# check_status = /home/oasis/oasis-node-admin/script/oasis.sh control status


def execute_remote_command_to_json(
    cmd,
    path,
    user="oasis",
    ip="127.0.0.1",
):
    logger.info("Command: " + user + "@" + ip + " " + " ".join(cmd))
    out = execute_remote_command_to_string(cmd, path, user, ip)
    # logger.info("Output: " + out)
    return json.loads(out)


def execute_remote_command_to_string(
    cmd,
    path,
    user="oasis",
    ip="127.0.0.1",
):
    result = execute_remote_command(cmd, path, user, ip)
    # logger.info(
    #     "Result: "
    #     + str(result.returncode)
    #     + " "
    #     + result.stdout
    #     + " "
    #     + result.stderr
    # )
    if result.returncode != 0:
        logger.error(
            "Error executing remote command: "
            + user
            + "@"
            + ip
            + ":"
            + path
            + " "
            + " ".join(cmd)
            + " "
            + result.stderr
        )
        raise Exception(
            "Error executing remote command: "
            + user
            + "@"
            + ip
            + ":"
            + path
            + " "
            + " ".join(cmd)
            + " "
            + result.stderr
        )
    return result.stdout


def execute_remote_command(
    command,
    path,
    user="oasis",
    ip="127.0.0.1",
):
    if command is None:
        raise Exception("Command is null")
    cmd = [
        "ssh",
        "-4",
        "-o",
        "StrictHostKeyChecking=accept-new",
        "-o",
        "ConnectTimeout=10",
        user + "@" + ip,
    ]
    cmd.extend(command)
    # logger.info("Command: " + " ".join(cmd))
    result = execute_command(cmd)
    return result


def execute_ansible_tasks(
    tasks,
    host_list=["127.0.0.1"],
):
    # since the API is constructed for CLI it expects certain options to always be set in the context object
    context.CLIARGS = ImmutableDict(
        connection="smart",
        module_path=[
            "/usr/lib/python3/dist-packages",
            "/usr/share/ansible",
        ],
        forks=10,
        become=None,
        become_method=None,
        become_user=None,
        check=False,
        diff=False,
        verbosity=0,
    )
    # required for
    # https://github.com/ansible/ansible/blob/devel/lib/ansible/inventory/manager.py#L204
    sources = ",".join(host_list)
    if len(host_list) == 1:
        sources += ","

    # initialize needed objects
    loader = (
        DataLoader()
    )  # Takes care of finding and reading yaml, json and ini files
    passwords = dict(vault_pass="secret")

    # Instantiate our ResultsCollectorJSONCallback for handling results as they come in. Ansible expects this to be one of its main display outlets
    results_callback = ResultsCollectorJSONCallback()

    # create inventory, use path to host config file as source or hosts in a comma separated string
    inventory = InventoryManager(loader=loader, sources=sources)

    # variable manager takes care of merging all the different sources to give you a unified view of variables available in each context
    variable_manager = VariableManager(loader=loader, inventory=inventory)

    # instantiate task queue manager, which takes care of forking and setting up all objects to iterate over host list and tasks
    # IMPORTANT: This also adds library dirs paths to the module loader
    # IMPORTANT: and so it must be initialized before calling `Play.load()`.
    tqm = TaskQueueManager(
        inventory=inventory,
        variable_manager=variable_manager,
        loader=loader,
        passwords=passwords,
        stdout_callback=results_callback,  # Use our custom callback instead of the ``default`` callback plugin, which prints to stdout
    )

    # create data structure that represents our play, including tasks, this is basically what our YAML loader does internally.
    play_source = dict(
        name="Ansible Play",
        hosts=host_list,
        gather_facts="no",
        tasks=tasks,
    )

    # Create play object, playbook objects use .load instead of init or new methods,
    # this will also automatically create the task objects from the info provided in play_source
    play = Play().load(
        play_source, variable_manager=variable_manager, loader=loader
    )

    # Actually run it
    try:
        result = tqm.run(
            play
        )  # most interesting data for a play is actually sent to the callback's methods
    finally:
        # we always need to cleanup child procs and the structures we use to communicate with them
        tqm.cleanup()
        if loader:
            loader.cleanup_all_tmp_files()

    # Remove ansible tmpdir
    shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

    print("UP ***********")
    for host, result in results_callback.host_ok.items():
        if "stdout" in result._result:
            print("{0} >>> {1}".format(host, result._result["stdout"]))

    print("FAILED *******")
    for host, result in results_callback.host_failed.items():
        print("{0} >>> {1}".format(host, result._result["msg"]))

    print("DOWN *********")
    for host, result in results_callback.host_unreachable.items():
        print("{0} >>> {1}".format(host, result._result["msg"]))


def execute_command(cmd):
    if cmd is None:
        raise Exception("Command is null")
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
    )
    """
    print("Out: \n" + result.stdout + "\n")
    print("Error: \n" + result.stderr + "\n")
    print("Return code: \n" + str(result.returncode) + "\n")
    """
    return result
