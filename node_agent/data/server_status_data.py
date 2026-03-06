from node_agent.model.db import db
from node_agent.model.server_status import ServerStatus


def server_status_data(server_id: int, status_fields: dict):
    server_status_db = ServerStatus(server_id=server_id)
    for key, value in status_fields.items():
        if hasattr(server_status_db, key):
            setattr(server_status_db, key, value)
    db.session.add(server_status_db)
    db.session.commit()


def server_status_data_get_lastest(server_id: int) -> dict:
    server_status_db = (
        db.session.query(ServerStatus)
        .filter(ServerStatus.server_id == server_id)
        .order_by(ServerStatus.time_updated.desc())
        .first()
    )
    if server_status_db is None:
        return None
    return server_status_db.to_dict()
