from node_agent.model.group import Group
from node_agent.model.user import User


def map_organization(organization) -> dict:
    if organization is None:
        return None
    return {
        "id": organization.id,
        "name": organization.name,
        "parent_id": organization.parent_id,
        "time_create": organization.time_create,
        "time_updated": organization.time_updated,
    }


def organization_data_create(
    name: str, parent_id: int = None, owner_id: int = None
) -> dict:
    from node_agent.model.organization import Organization
    from node_agent.model.db import db

    organization = Organization(name=name, parent_id=parent_id)
    db.session.add(organization)

    # Force INSERT so the DB-generated primary key is available immediately.
    db.session.commit()
    if organization.id is None:
        raise ValueError("organization id was not generated")

    group = Group(name="admin", organization_id=organization.id)
    db.session.add(group)
    if owner_id is not None:

        user = db.session.query(User).filter_by(id=owner_id).first()
        if user is not None:
            user.groups.append(group)

    db.session.commit()
    return map_organization(organization)
