import logging

from node_agent.model.db import db
from node_agent.model.server import Server
from node_agent.model.server_host import ServerHost
from node_agent.model.server_port import ServerPort
from node_agent.model.server_ssh import ServerSSH

logger = logging.getLogger(__name__)


def map_server_with_ssh(server_db) -> dict:
    if server_db is None:
        return None
    server = {"id": server_db.id, "name": server_db.name}
    server_host_db_list = (
        db.session.query(ServerHost)
        .filter(ServerHost.server_id == server_db.id)
        .all()
    )
    server["ssh"] = []
    for server_host_db in server_host_db_list:
        server_port_db_list = (
            db.session.query(ServerPort)
            .filter(ServerPort.server_host_id == server_host_db.id)
            .all()
        )
        for server_port_db in server_port_db_list:
            server_ssh_db_list = (
                db.session.query(ServerSSH)
                .filter(ServerSSH.server_port_id == server_port_db.id)
                .all()
            )
            for server_ssh_db in server_ssh_db_list:
                server_ssh = {
                    "host": server_host_db.name,
                    "port": server_port_db.port,
                    "user_name": server_ssh_db.user_name,
                }
                server["ssh"].append(server_ssh)
    return server


def map_server(server) -> dict:
    if server is None:
        return None
    return {
        "id": server.id,
        "name": server.name,
        "cloud": server.cloud,
        "cloud_name": server.cloud_name,
        "ip": server.ip,
        "hostname": server.hostname,
        "fqdn": server.fqdn,
        "os": server.os,
        "kernel": server.kernel,
        "cpu_cores": server.cpu_cores,
        "ram_total_mb": server.ram_total_mb,
        "organization_id": server.organization_id,
        "time_create": server.time_create,
        "time_updated": server.time_updated,
    }


def map_server_host(server_host) -> dict:
    if server_host is None:
        return None
    return {
        "id": server_host.id,
        "name": server_host.name,
        "description": server_host.description,
        "server_id": server_host.server_id,
        "time_create": server_host.time_create,
        "time_updated": server_host.time_updated,
    }


def map_server_port(server_port) -> dict:
    if server_port is None:
        return None
    return {
        "id": server_port.id,
        "port": server_port.port,
        "description": server_port.description,
        "server_host_id": server_port.server_host_id,
        "time_create": server_port.time_create,
        "time_updated": server_port.time_updated,
    }


def map_server_ssh(server_ssh) -> dict:
    if server_ssh is None:
        return None
    return {
        "id": server_ssh.id,
        "user_name": server_ssh.user_name,
        "description": server_ssh.description,
        "server_port_id": server_ssh.server_port_id,
        "time_create": server_ssh.time_create,
        "time_updated": server_ssh.time_updated,
    }


def server_data_create(
    name: str,
    organization_id: int = None,
    ip: str = None,
    cloud: str = None,
    cloud_name: str = None,
    hostname: str = None,
    fqdn: str = None,
    os: str = None,
    kernel: str = None,
    cpu_cores: int = None,
    ram_total_mb: int = None,
) -> dict:
    if organization_id is None:
        raise ValueError("organization_id is required")

    # Build first, then set FK explicitly to avoid dataclass relationship
    # default (organization=None) overriding the FK at init time.
    server = Server(
        name=name,
        ip=ip,
        cloud=cloud,
        cloud_name=cloud_name,
        hostname=hostname,
        fqdn=fqdn,
        os=os,
        kernel=kernel,
        cpu_cores=cpu_cores,
        ram_total_mb=ram_total_mb,
    )
    server.organization_id = organization_id
    db.session.add(server)
    db.session.commit()
    return map_server(server)


def server_host_data_create(
    server_id: int,
    name: str = None,
    description: str = None,
) -> dict:
    server_host = ServerHost(
        server_id=server_id,
        name=name,
        description=description,
    )
    db.session.add(server_host)
    db.session.commit()
    return map_server_host(server_host)


def server_port_data_create(
    server_host_id: int,
    port: str = None,
    description: str = None,
) -> dict:
    server_port = ServerPort(
        server_host_id=server_host_id,
        port=port,
        description=description,
    )
    db.session.add(server_port)
    db.session.commit()
    return map_server_port(server_port)


def server_ssh_data_create(
    server_port_id: int,
    user_name: str = None,
    description: str = None,
) -> dict:
    server_ssh = ServerSSH(
        server_port_id=server_port_id,
        user_name=user_name,
        description=description,
    )
    db.session.add(server_ssh)
    db.session.commit()
    return map_server_ssh(server_ssh)


def server_data_update(server_id: int, static_fields: dict) -> dict:
    server = db.session.query(Server).filter(Server.id == server_id).first()
    if server is None:
        raise ValueError(f"server_id={server_id} not found")

    static_fields = static_fields or {}

    if "hostname" in static_fields:
        server.hostname = static_fields.get("hostname")
    if "fqdn" in static_fields:
        server.fqdn = static_fields.get("fqdn")
    if "ip" in static_fields:
        server.ip = static_fields.get("ip")
    if "os" in static_fields:
        server.os = static_fields.get("os")
    if "kernel" in static_fields:
        server.kernel = static_fields.get("kernel")

    cpu_cores = static_fields.get("cpu_cores")
    if cpu_cores is not None:
        try:
            server.cpu_cores = int(str(cpu_cores))
        except (TypeError, ValueError):
            server.cpu_cores = None

    ram_total_mb = static_fields.get("ram_total_mb")
    if ram_total_mb is not None:
        try:
            server.ram_total_mb = int(str(ram_total_mb))
        except (TypeError, ValueError):
            server.ram_total_mb = None

    db.session.commit()
    return map_server(server)


def server_ssh_data_create_full(
    server_name: str,
    organization_id: int,
    server_ip: str = None,
    cloud: str = None,
    cloud_name: str = None,
    hostname: str = None,
    fqdn: str = None,
    os: str = None,
    kernel: str = None,
    cpu_cores: int = None,
    ram_total_mb: int = None,
    host_name: str = None,
    host_description: str = None,
    port: str = None,
    port_description: str = None,
    ssh_user_name: str = None,
    ssh_description: str = None,
) -> dict:

    # Build first, then set FK explicitly to avoid dataclass relationship
    # default (organization=None) overriding the FK at init time.
    server = Server(
        name=server_name,
        organization_id=organization_id,
        ip=server_ip,
        cloud=cloud,
        cloud_name=cloud_name,
        hostname=hostname,
        fqdn=fqdn,
        os=os,
        kernel=kernel,
        cpu_cores=cpu_cores,
        ram_total_mb=ram_total_mb,
    )
    db.session.add(server)
    db.session.flush()

    server_host = ServerHost(
        server_id=server.id,
        name=host_name,
        description=host_description,
    )
    db.session.add(server_host)
    db.session.flush()

    server_port = ServerPort(
        server_host_id=server_host.id,
        port=port,
        description=port_description,
    )
    db.session.add(server_port)
    db.session.flush()

    server_ssh = ServerSSH(
        server_port_id=server_port.id,
        user_name=ssh_user_name,
        description=ssh_description,
    )
    db.session.add(server_ssh)
    db.session.commit()

    return {
        "server": map_server(server),
        "server_host": map_server_host(server_host),
        "server_port": map_server_port(server_port),
        "server_ssh": map_server_ssh(server_ssh),
    }


def get_server_ssh_map(organization_id: int) -> dict:
    servers = (
        db.session.query(Server)
        .filter(Server.organization_id == organization_id)
        .all()
    )

    return [map_server_with_ssh(server) for server in servers]


def get_server_ssh(organization_id: int) -> dict:
    list = get_server_ssh_map(organization_id)
    server_list = {}
    for server in list:
        logger.info(server)
        for ssh in server["ssh"]:
            ssh_str = ssh["host"]
            if ssh["port"] is not None and ssh["port"] != "22":
                ssh_str += f":{ssh['port']}"
            if ssh["user_name"] is not None:
                ssh_str = f"{ssh['user_name']}@{ssh_str}"
                server_list.setdefault(server["id"], ssh_str)
    return server_list


def server_data_get_server(server_id: int):
    server_db = db.session.query(Server).filter(Server.id == server_id).first()
    return map_server(server_db)
