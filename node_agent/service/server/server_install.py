import logging

from node_agent.shell.shell import execute_ansible_tasks

logger = logging.getLogger()


def server_install_package(package_name: str, entrypoint: dict) -> None:
    logger.info(f"Entry point: {entrypoint}")
    ip = entrypoint["server"]["ip"]
    if not ip:
        raise Exception("Remote node entrypoint/server/ip is not defined")
    """Install the package with the given name."""
    package_name = package_name.lower()
    execute_ansible_tasks(
        [
            {
                "action": {
                    "module": "apt",
                    "args": {
                        "name": package_name,
                        "state": "latest",
                    },
                },
            }
        ],
        [ip],
    )
