#!/usr/bin/env python

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from node_agent.ansible.ansible_playbook import AnsiblePlaybook


def _to_int(value: Any) -> Optional[int]:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return None


def _parse_load_avg(raw: str) -> List[float]:
    values = []
    for part in str(raw).split()[:3]:
        try:
            values.append(float(part))
        except ValueError:
            continue
    return values


def _flatten_load_avg(raw: str) -> Dict[str, Optional[float]]:
    parsed = _parse_load_avg(raw)
    return {
        "load_avg_1m": parsed[0] if len(parsed) > 0 else None,
        "load_avg_5m": parsed[1] if len(parsed) > 1 else None,
        "load_avg_15m": parsed[2] if len(parsed) > 2 else None,
    }


def _parse_memory_usage(lines: Any) -> Dict[str, Any]:
    if not isinstance(lines, list):
        return {}

    result: Dict[str, Any] = {}
    for line in lines:
        if not isinstance(line, str):
            continue
        parts = line.split()
        if not parts:
            continue

        if parts[0] == "Mem:" and len(parts) >= 7:
            result["mem"] = {
                "total_mb": _to_int(parts[1]),
                "used_mb": _to_int(parts[2]),
                "free_mb": _to_int(parts[3]),
                "shared_mb": _to_int(parts[4]),
                "buff_cache_mb": _to_int(parts[5]),
                "available_mb": _to_int(parts[6]),
            }

        if parts[0] == "Swap:" and len(parts) >= 4:
            result["swap"] = {
                "total_mb": _to_int(parts[1]),
                "used_mb": _to_int(parts[2]),
                "free_mb": _to_int(parts[3]),
            }

    return result


def _flatten_memory_metrics(
    memory: Dict[str, Any],
) -> Dict[str, Optional[int]]:
    mem = memory.get("mem", {}) if isinstance(memory, dict) else {}
    swap = memory.get("swap", {}) if isinstance(memory, dict) else {}

    return {
        "memory_total_mb": _to_int(mem.get("total_mb")),
        "memory_used_mb": _to_int(mem.get("used_mb")),
        "memory_free_mb": _to_int(mem.get("free_mb")),
        "memory_shared_mb": _to_int(mem.get("shared_mb")),
        "memory_buff_cache_mb": _to_int(mem.get("buff_cache_mb")),
        "memory_available_mb": _to_int(mem.get("available_mb")),
        "swap_total_mb": _to_int(swap.get("total_mb")),
        "swap_used_mb": _to_int(swap.get("used_mb")),
        "swap_free_mb": _to_int(swap.get("free_mb")),
    }


def _parse_disk_usage(lines: Any) -> List[Dict[str, Any]]:
    if not isinstance(lines, list) or len(lines) < 2:
        return []

    disks: List[Dict[str, Any]] = []
    for line in lines[1:]:
        if not isinstance(line, str):
            continue

        parts = line.split()
        if len(parts) < 6:
            continue

        disks.append(
            {
                "filesystem": parts[0],
                "size": parts[1],
                "used": parts[2],
                "available": parts[3],
                "use_percent": parts[4],
                "mount": parts[5],
            }
        )

    return disks


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


def retrieve_server_dynamic(
    hosts: Optional[List[str]] = None,
    inventory: str = "",
    service_to_check: str = "sshd",
    include_raw: bool = False,
) -> Dict[str, Any]:
    tasks = [
        dict(
            name="Get uptime",
            action=dict(module="command", args=dict(cmd="uptime -p")),
            register="uptime_result",
            changed_when=False,
        ),
        dict(
            name="Get load average",
            action=dict(module="command", args=dict(cmd="cat /proc/loadavg")),
            register="load_result",
            changed_when=False,
        ),
        dict(
            name="Get disk usage",
            action=dict(module="command", args=dict(cmd="df -hP")),
            register="disk_result",
            changed_when=False,
        ),
        dict(
            name="Get memory usage",
            action=dict(module="command", args=dict(cmd="free -m")),
            register="memory_result",
            changed_when=False,
        ),
        dict(
            name="Collect service facts", action=dict(module="service_facts")
        ),
        dict(
            name="Collect dynamic server information",
            action=dict(
                module="debug",
                args=dict(
                    msg=dict(
                        uptime="{{ uptime_result.stdout }}",
                        load_avg="{{ load_result.stdout }}",
                        disk_usage="{{ disk_result.stdout_lines }}",
                        memory_usage="{{ memory_result.stdout_lines }}",
                        service_state=(
                            "{{ ansible_facts.services[service_to_check + '.service'].state "
                            "| default('unknown') }}"
                        ),
                        service_status=(
                            "{{ ansible_facts.services[service_to_check + '.service'].status "
                            "| default('unknown') }}"
                        ),
                    )
                ),
            ),
        ),
    ]

    playbook = AnsiblePlaybook(
        name="Retrieve dynamic server state",
        hosts=hosts or [],
        inventory=inventory,
        play_vars={"service_to_check": service_to_check},
        gather_facts="no",
        become=False,
        tasks=tasks,
    )

    output = playbook.play()

    hosts_data: List[Dict[str, Any]] = []
    for host, host_result in output["ok"].items():
        msg = host_result.get("msg")
        if isinstance(msg, dict):
            service_state = msg.get("service_state")
            service_status = msg.get("service_status")
            status_value = (
                str(service_status).lower()
                if service_status is not None
                else ""
            )
            disks = _parse_disk_usage(msg.get("disk_usage", []))
            memory_metrics = _flatten_memory_metrics(
                _parse_memory_usage(msg.get("memory_usage", []))
            )

            record = {
                "target": host,
                "static_fields": {},
                "dynamic_fields": {
                    "uptime": msg.get("uptime"),
                    **_flatten_load_avg(str(msg.get("load_avg", ""))),
                    "disks": disks,
                    **memory_metrics,
                    "service_state": service_state,
                    "service_status": service_status,
                    "health": {
                        "reachable": True,
                        "service_active": service_state == "active",
                        "service_status_ok": status_value
                        in ("running", "enabled", "active", "alias"),
                    },
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
                    "health": {"reachable": True},
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
