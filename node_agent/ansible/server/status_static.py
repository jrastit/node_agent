#!/usr/bin/env python

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union

from node_agent.ansible.ansible_playbook import AnsiblePlaybook


def _flatten_host_errors(
    errors: Dict[str, Dict[str, Any]],
) -> List[Dict[str, Any]]:
    return [
        {
            "target": host,
            "msg": data.get("msg"),
            "stdout": data.get("stdout"),
            "stderr": data.get("stderr"),
        }
        for host, data in errors.items()
    ]


def _to_int(value: Any) -> Optional[int]:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return None


def _get_task_result(
    entries: List[Dict[str, Any]],
    task_name: str,
) -> Dict[str, Any]:
    for entry in reversed(entries):
        if entry.get("task") == task_name and isinstance(
            entry.get("result"), dict
        ):
            return entry["result"]
    return {}


def retrieve_server_static(
    hosts: Optional[List[str]] = None,
    inventory: str = "",
    service_to_check: Union[str, List[str]] = "sshd",
    include_raw: bool = False,
) -> Dict[str, Any]:
    tasks: List[Dict[str, Any]] = []

    playbook = AnsiblePlaybook(
        name="Retrieve static server state",
        hosts=hosts or [],
        inventory=inventory,
        play_vars={"service_to_check": service_to_check},
        gather_facts="yes",
        become=False,
        tasks=tasks,
    )

    output = playbook.play()
    ok_history = output.get("ok_history", {})

    hosts_data: List[Dict[str, Any]] = []
    for host, entries in ok_history.items():
        if not isinstance(entries, list):
            entries = []

        fact_result = _get_task_result(entries, "Gathering Facts")
        facts = fact_result.get("ansible_facts", {})
        if not isinstance(facts, dict):
            facts = {}

        default_ipv4 = facts.get("ansible_default_ipv4", {})
        ip_address = "N/A"
        if isinstance(default_ipv4, dict):
            ip_address = str(default_ipv4.get("address", "N/A"))

        static_fields = {
            "hostname": facts.get("ansible_hostname"),
            "fqdn": facts.get("ansible_fqdn"),
            "ip": ip_address,
            "os": "{} {}".format(
                facts.get("ansible_distribution", ""),
                facts.get("ansible_distribution_version", ""),
            ).strip(),
            "kernel": facts.get("ansible_kernel"),
            "cpu_cores": _to_int(facts.get("ansible_processor_vcpus")),
            "ram_total_mb": _to_int(facts.get("ansible_memtotal_mb")),
            "service_name": service_to_check,
        }

        record = {
            "target": host,
            "static_fields": static_fields,
            "dynamic_fields": {
                "collected_at": datetime.now(timezone.utc).isoformat(),
            },
        }
        if include_raw:
            record["raw"] = facts
        hosts_data.append(record)

    failed = _flatten_host_errors(output["failed"])
    unreachable = _flatten_host_errors(output["unreachable"])

    return {
        "meta": {
            "ok_count": len(hosts_data),
            "failed_count": len(failed),
            "unreachable_count": len(unreachable),
            "total_count": len(hosts_data) + len(failed) + len(unreachable),
        },
        "hosts": hosts_data,
        "errors": {
            "failed": failed,
            "unreachable": unreachable,
        },
    }
