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


def retrieve_server_static(
    hosts: Optional[List[str]] = None,
    inventory: str = "",
    service_to_check: Union[str, List[str]] = "sshd",
    include_raw: bool = False,
) -> Dict[str, Any]:
    tasks = [
        dict(
            name="Collect static server information",
            action=dict(
                module="debug",
                args=dict(
                    msg=dict(
                        hostname="{{ ansible_hostname }}",
                        fqdn="{{ ansible_fqdn }}",
                        ip="{{ ansible_default_ipv4.address | default('N/A') }}",
                        os="{{ ansible_distribution }} {{ ansible_distribution_version }}",
                        kernel="{{ ansible_kernel }}",
                        cpu_cores="{{ ansible_processor_vcpus | default('N/A') }}",
                        ram_total_mb="{{ ansible_memtotal_mb }}",
                        service_name="{{ service_to_check }}",
                    )
                ),
            ),
        ),
    ]

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

    hosts_data: List[Dict[str, Any]] = []
    for host, host_result in output["ok"].items():
        msg = host_result.get("msg")
        if isinstance(msg, dict):
            record = {
                "target": host,
                "static_fields": msg,
                "dynamic_fields": {
                    "collected_at": datetime.now(timezone.utc).isoformat(),
                },
            }
            if include_raw:
                record["raw"] = msg
            hosts_data.append(record)
        else:
            fallback = {
                "target": host,
                "static_fields": {},
                "dynamic_fields": {
                    "collected_at": datetime.now(timezone.utc).isoformat(),
                },
            }
            if include_raw:
                fallback["raw"] = host_result
            hosts_data.append(fallback)

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
