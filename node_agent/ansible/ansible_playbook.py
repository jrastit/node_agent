#!/usr/bin/env python

import shutil
from typing import Any, Dict, List, Optional

import ansible.constants as C
from ansible import context
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory.manager import InventoryManager
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.plugins.loader import init_plugin_loader
from ansible.playbook.play import Play
from ansible.utils.collection_loader import AnsibleCollectionConfig
from ansible.vars.manager import VariableManager

from node_agent.ansible.results_collector_JSON_callback import (
    ResultsCollectorJSONCallback,
)


class AnsiblePlaybook:
    def __init__(
        self,
        name: str = "",
        hosts: Optional[List[str]] = None,
        inventory: str = "",
        tasks: Optional[List[Dict[str, Any]]] = None,
        play_vars: Optional[Dict[str, Any]] = None,
        gather_facts: str = "",
        connection: str = "",
        module_path: Optional[List[str]] = None,
        forks: Optional[int] = None,
        become: Optional[bool] = None,
        become_method: Optional[str] = None,
        become_user: Optional[str] = None,
        check: Optional[bool] = None,
        diff: Optional[bool] = None,
        verbosity: Optional[int] = None,
        passwords: Optional[Dict[str, str]] = None,
    ):
        # Keep all fields empty/default so callers can set them explicitly.
        self.name = name
        self.hosts = hosts or []
        self.inventory = inventory
        self.tasks = tasks or []
        self.play_vars = play_vars or {}
        self.gather_facts = gather_facts
        self.connection = connection
        self.module_path = module_path or []
        self.forks = forks
        self.become = become
        self.become_method = become_method
        self.become_user = become_user
        self.check = check
        self.diff = diff
        self.verbosity = verbosity
        self.passwords = passwords or {}

    def set_hosts(self, hosts: List[str]) -> "AnsiblePlaybook":
        self.hosts = hosts
        return self

    def set_inventory(self, inventory: str) -> "AnsiblePlaybook":
        self.inventory = inventory
        return self

    def set_tasks(self, tasks: List[Dict[str, Any]]) -> "AnsiblePlaybook":
        self.tasks = tasks
        return self

    def set_play_vars(self, play_vars: Dict[str, Any]) -> "AnsiblePlaybook":
        self.play_vars = play_vars
        return self

    def set_name(self, name: str) -> "AnsiblePlaybook":
        self.name = name
        return self

    def _get_inventory_source(self) -> str:
        if self.inventory:
            return self.inventory

        if not self.hosts:
            raise ValueError(
                "Set `hosts` or `inventory` before calling play()."
            )

        sources = ",".join(self.hosts)
        if len(self.hosts) == 1:
            sources += ","
        return sources

    def _build_cli_args(self) -> None:
        effective_become_method = (
            (self.become_method if self.become_method else "sudo")
            if self.become
            else None
        )

        context.CLIARGS = ImmutableDict(
            connection=self.connection or "smart",
            module_path=self.module_path
            or [
                "/usr/lib/python3/dist-packages",
                "/usr/share/ansible",
            ],
            forks=self.forks if self.forks is not None else 10,
            become=self.become,
            become_method=effective_become_method,
            become_user=self.become_user,
            check=self.check if self.check is not None else False,
            diff=self.diff if self.diff is not None else False,
            verbosity=self.verbosity if self.verbosity is not None else 0,
        )

    def play(self) -> Dict[str, Any]:
        self._build_cli_args()
        sources = self._get_inventory_source()

        if AnsibleCollectionConfig.collection_finder is None:
            init_plugin_loader()

        loader = DataLoader()
        passwords = self.passwords or dict(vault_pass="secret")
        results_callback = ResultsCollectorJSONCallback()

        inventory = InventoryManager(loader=loader, sources=sources)
        variable_manager = VariableManager(loader=loader, inventory=inventory)

        tqm = TaskQueueManager(
            inventory=inventory,
            variable_manager=variable_manager,
            loader=loader,
            passwords=passwords,
            stdout_callback_name="default",
        )
        tqm.load_callbacks()
        results_callback._init_callback_methods()
        results_callback.set_options()
        tqm._callback_plugins.append(results_callback)

        play_source = dict(
            name=self.name or "Ansible Play",
            hosts=self.hosts or ["all"],
            gather_facts=self.gather_facts or "no",
            vars=self.play_vars,
            tasks=self.tasks,
        )

        if self.become is not None:
            play_source["become"] = self.become
            play_source["become_method"] = (
                self.become_method if self.become_method else "sudo"
            )
            if self.become_user:
                play_source["become_user"] = self.become_user

        play = Play().load(
            play_source, variable_manager=variable_manager, loader=loader
        )

        try:
            result = tqm.run(play)
        finally:
            tqm.cleanup()
            loader.cleanup_all_tmp_files()

        shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

        return {
            "result": result,
            "ok": {
                host: data._result
                for host, data in results_callback.host_ok.items()
            },
            "failed": {
                host: data._result
                for host, data in results_callback.host_failed.items()
            },
            "unreachable": {
                host: data._result
                for host, data in results_callback.host_unreachable.items()
            },
        }
