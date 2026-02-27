from node_agent.model.group import Group


def map_organisation(organisation) -> dict:
    if organisation is None:
        return None
    return {
        "id": organisation.id,
        "name": organisation.name,
        "parent_id": organisation.parent_id,
        "time_create": organisation.time_create,
        "time_updated": organisation.time_updated,
    }


def organisation_data_create(
    name: str, parent_id: int = None, owner_id: int = None
) -> dict:
    from node_agent.model.organisation import Organisation
    from node_agent.model.db import db

    organisation = Organisation(name=name, parent_id=parent_id)
    db.session.add(organisation)
    group = Group(name=f"admin", organisation=organisation)
    db.session.add(group)
    if owner_id is not None:
        from node_agent.model.user import User
        from node_agent.model.db import db

        user = db.session.query(User).filter_by(id=owner_id).first()
        if user is not None:
            user.groups.append(group)

    db.session.commit()
    return map_organisation(organisation)
