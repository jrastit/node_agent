#!/usr/bin/env python

from typing import Any, Dict, List, Optional, Union

from node_agent.ansible.server.status_dynamic import retrieve_server_dynamic
from node_agent.ansible.server.status_static import retrieve_server_static


def _index_hosts_by_target(
    hosts: List[Dict[str, Any]],
) -> Dict[str, Dict[str, Any]]:
    indexed: Dict[str, Dict[str, Any]] = {}
    for item in hosts:
        target = item.get("target")
        if not target:
            continue
        indexed[target] = item
    return indexed


def _merge_host_records(
    static_hosts: List[Dict[str, Any]],
    dynamic_hosts: List[Dict[str, Any]],
    include_raw: bool,
) -> List[Dict[str, Any]]:
    merged: Dict[str, Dict[str, Any]] = {}

    for target, item in _index_hosts_by_target(static_hosts).items():
        merged[target] = {
            "target": target,
            "static_fields": dict(item.get("static_fields", {})),
            "dynamic_fields": dict(item.get("dynamic_fields", {})),
        }
        if include_raw and "raw" in item:
            merged[target]["raw"] = {"static": item["raw"]}

    for target, item in _index_hosts_by_target(dynamic_hosts).items():
        if target not in merged:
            merged[target] = {
                "target": target,
                "static_fields": {},
                "dynamic_fields": {},
            }

        merged[target]["static_fields"].update(item.get("static_fields", {}))
        merged[target]["dynamic_fields"].update(item.get("dynamic_fields", {}))

        if include_raw and "raw" in item:
            raw_holder = merged[target].setdefault("raw", {})
            if isinstance(raw_holder, dict):
                raw_holder["dynamic"] = item["raw"]

    return list(merged.values())


def retrieve_server_state(
    hosts: Optional[List[str]] = None,
    inventory: str = "",
    service_to_check: Union[str, List[str]] = "sshd",
    include_raw: bool = False,
) -> Dict[str, Any]:
    static_result = retrieve_server_static(
        hosts=hosts,
        inventory=inventory,
        service_to_check=service_to_check,
        include_raw=include_raw,
    )
    dynamic_result = retrieve_server_dynamic(
        hosts=hosts,
        inventory=inventory,
        service_to_check=service_to_check,
        include_raw=include_raw,
    )

    merged_hosts = _merge_host_records(
        static_result.get("hosts", []),
        dynamic_result.get("hosts", []),
        include_raw,
    )

    static_errors = static_result.get("errors", {})
    dynamic_errors = dynamic_result.get("errors", {})

    failed = list(static_errors.get("failed", [])) + list(
        dynamic_errors.get("failed", [])
    )
    unreachable = list(static_errors.get("unreachable", [])) + list(
        dynamic_errors.get("unreachable", [])
    )

    return {
        "meta": {
            "ok_count": len(merged_hosts),
            "failed_count": len(failed),
            "unreachable_count": len(unreachable),
            "total_count": len(merged_hosts) + len(failed) + len(unreachable),
            "runs": {
                "static": static_result.get("meta", {}),
                "dynamic": dynamic_result.get("meta", {}),
            },
        },
        "hosts": merged_hosts,
        "errors": {
            "failed": failed,
            "unreachable": unreachable,
            "static": static_errors,
            "dynamic": dynamic_errors,
        },
    }


__all__ = [
    "retrieve_server_state",
    "retrieve_server_static",
    "retrieve_server_dynamic",
]
