#!/usr/bin/env python

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union

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


def _normalize_service_names(
    service_to_check: Union[str, List[str], None],
) -> List[str]:
    if service_to_check is None:
        return ["sshd"]

    if isinstance(service_to_check, str):
        return [service_to_check]

    normalized: List[str] = []
    for name in service_to_check:
        if isinstance(name, str) and name.strip():
            normalized.append(name)
    return normalized or ["sshd"]


def _parse_services(
    active_results: Any,
    enabled_results: Any,
) -> List[Dict[str, Any]]:
    def _normalize_output(value: Any) -> str:
        text = str(value or "").strip()
        if not text:
            return "unknown"

        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if not lines:
            return "unknown"

        # Some environments may return duplicated lines; keep first meaningful one.
        return lines[0]

    active_map: Dict[str, Dict[str, Any]] = {}
    enabled_map: Dict[str, Dict[str, Any]] = {}

    if isinstance(active_results, list):
        for item in active_results:
            if not isinstance(item, dict):
                continue
            service = item.get("item")
            if isinstance(service, str):
                active_map[service] = item

    if isinstance(enabled_results, list):
        for item in enabled_results:
            if not isinstance(item, dict):
                continue
            service = item.get("item")
            if isinstance(service, str):
                enabled_map[service] = item

    services: List[Dict[str, Any]] = []
    for service in sorted(set(active_map.keys()) | set(enabled_map.keys())):
        active_item = active_map.get(service, {})
        enabled_item = enabled_map.get(service, {})

        state = _normalize_output(active_item.get("stdout", "unknown"))
        status = _normalize_output(enabled_item.get("stdout", "unknown"))

        services.append(
            {
                "name": service,
                "state": state,
                "status": status,
                "active_rc": active_item.get("rc"),
                "enabled_rc": enabled_item.get("rc"),
            }
        )

    return services


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


def retrieve_server_dynamic(
    hosts: Optional[List[str]] = None,
    inventory: str = "",
    service_to_check: Union[str, List[str]] = "sshd",
    include_raw: bool = False,
) -> Dict[str, Any]:
    service_names = _normalize_service_names(service_to_check)

    tasks = [
        {
            "name": "Get uptime",
            "action": "ansible.builtin.command",
            "args": {"cmd": "uptime -p"},
            "register": "uptime_result",
            "changed_when": False,
        },
        {
            "name": "Get load average",
            "action": "ansible.builtin.command",
            "args": {"cmd": "cat /proc/loadavg"},
            "register": "load_result",
            "changed_when": False,
        },
        {
            "name": "Get disk usage",
            "action": "ansible.builtin.command",
            "args": {"cmd": "df -hP"},
            "register": "disk_result",
            "changed_when": False,
        },
        {
            "name": "Get memory usage",
            "action": "ansible.builtin.command",
            "args": {"cmd": "free -m"},
            "register": "memory_result",
            "changed_when": False,
        },
        {
            "name": "Get service active states",
            "action": "ansible.builtin.command",
            "args": {"cmd": "systemctl is-active {{ item }}"},
            "loop": service_names,
            "register": "service_active_results",
            "changed_when": False,
            "failed_when": False,
        },
        {
            "name": "Get service enabled states",
            "action": "ansible.builtin.command",
            "args": {"cmd": "systemctl is-enabled {{ item }}"},
            "loop": service_names,
            "register": "service_enabled_results",
            "changed_when": False,
            "failed_when": False,
        },
    ]

    playbook = AnsiblePlaybook(
        name="Retrieve dynamic server state",
        hosts=hosts or [],
        inventory=inventory,
        play_vars={"service_to_check": service_names},
        gather_facts="no",
        become=False,
        tasks=tasks,
    )

    output = playbook.play()
    ok_history = output.get("ok_history", {})

    hosts_data: List[Dict[str, Any]] = []
    for host, entries in ok_history.items():
        if not isinstance(entries, list):
            entries = []

        uptime_result = _get_task_result(entries, "Get uptime")
        load_result = _get_task_result(entries, "Get load average")
        disk_result = _get_task_result(entries, "Get disk usage")
        memory_result = _get_task_result(entries, "Get memory usage")
        active_result = _get_task_result(entries, "Get service active states")
        enabled_result = _get_task_result(
            entries, "Get service enabled states"
        )

        disks = _parse_disk_usage(disk_result.get("stdout_lines", []))
        memory_metrics = _flatten_memory_metrics(
            _parse_memory_usage(memory_result.get("stdout_lines", []))
        )
        services = _parse_services(
            active_result.get("results"),
            enabled_result.get("results"),
        )

        all_service_active = (
            all(service.get("state") == "active" for service in services)
            if services
            else False
        )
        all_service_status_ok = (
            all(
                str(service.get("status", "")).lower()
                in (
                    "enabled",
                    "running",
                    "active",
                    "alias",
                    "static",
                    "indirect",
                )
                for service in services
            )
            if services
            else False
        )

        record = {
            "target": host,
            "static_fields": {},
            "dynamic_fields": {
                "uptime": uptime_result.get("stdout"),
                **_flatten_load_avg(str(load_result.get("stdout", ""))),
                "disks": disks,
                **memory_metrics,
                "services": services,
                "health_reachable": True,
                "health_service_active": all_service_active,
                "health_service_status_ok": all_service_status_ok,
                "collected_at": datetime.now(timezone.utc).isoformat(),
            },
        }
        if include_raw:
            record["raw"] = {
                "uptime": uptime_result,
                "load": load_result,
                "disk": disk_result,
                "memory": memory_result,
                "service_active": active_result,
                "service_enabled": enabled_result,
            }
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
