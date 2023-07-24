from node_agent.model.db import db
from flask import jsonify


def inset_or_update_object_from_json(mapper, data):
    if 'id' not in data or not data['id']:
        # user = User(**{k: v for k, v in obj.items() if k in {'id', 'name'}})
        db.session.bulk_insert_mappings(mapper, [data])
    else:
        db.session.bulk_update_mappings(mapper, [data])
    db.session.commit()
    server = db.session.query(mapper).filter_by(name=data['name']).first()
    return jsonify({mapper.__name__: server})


def get_object_list(mapper):
    return jsonify({mapper.__name__: db.session.query(mapper).all()})


def delete_object(mapper, id):
    db.session.query(mapper).filter_by(id=id).delete()
    db.session.commit()
    return {"Status": "success"}
