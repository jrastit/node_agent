from node_agent.model.db import db
from node_agent.model.server import Server
from node_agent.model.server_host import ServerHost
from node_agent.model.server_port import ServerPort
from node_agent.model.server_ssh import ServerSSH


def map_server(server) -> dict:
    if server is None:
        return None
    return {
        "id": server.id,
        "name": server.name,
        "cloud": server.cloud,
        "cloud_name": server.cloud_name,
        "ip": server.ip,
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


def server_ssh_data_create_full(
    server_name: str,
    organization_id: int,
    server_ip: str = None,
    cloud: str = None,
    cloud_name: str = None,
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
