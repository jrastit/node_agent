from node_agent.model.db import db
from datetime import date, datetime


def _serialize_value(value, visited):
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, list):
        return [_serialize_model(item, visited) for item in value]
    if hasattr(value, "__mapper__"):
        return _serialize_model(value, visited)
    return value


def _serialize_model(obj, visited=None):
    if obj is None:
        return None

    if visited is None:
        visited = set()

    marker = (obj.__class__.__name__, id(obj))
    if marker in visited:
        return {"id": getattr(obj, "id", None)}
    visited.add(marker)

    mapper = obj.__mapper__
    payload = {}

    for column in mapper.columns:
        payload[column.key] = _serialize_value(
            getattr(obj, column.key), visited
        )

    for relationship in mapper.relationships:
        payload[relationship.key] = _serialize_value(
            getattr(obj, relationship.key), visited
        )

    return payload


def inset_or_update_object_from_json_raw(mapper, data):
    if "id" not in data or not data["id"]:
        # user = User(**{k: v for k, v in obj.items() if k in {'id', 'name'}})
        db.session.bulk_insert_mappings(mapper, [data])
    else:
        db.session.bulk_update_mappings(mapper, [data])
    db.session.commit()
    ret = db.session.query(mapper).filter_by(name=data["name"]).first()
    return ret


def inset_or_update_object_from_json(mapper, data):
    obj = inset_or_update_object_from_json_raw(mapper, data)
    return {mapper.__name__: _serialize_model(obj)}


def get_object_list(mapper):
    return {
        mapper.__name__: [
            _serialize_model(obj) for obj in db.session.query(mapper).all()
        ]
    }


def delete_object(mapper, id):
    db.session.query(mapper).filter_by(id=id).delete()
    db.session.commit()
    return {"Status": "success"}
