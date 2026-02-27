from node_agent.model.user import User
from node_agent.model.db import db


def map_user(user_db):
    if user_db is None:
        return None
    return {
        "id": user_db.id,
        "auth_user_id": user_db.auth_user_id,
        "time_create": user_db.time_create,
        "time_updated": user_db.time_updated,
    }


def get_user_from_supabase(supabase_user):
    if supabase_user.id is None:
        return None
    user = (
        db.session.query(User).filter_by(auth_user_id=supabase_user.id).first()
    )
    if user is None:
        user = User(
            auth_user_id=supabase_user.id,
        )
        db.session.add(user)
        db.session.commit()

    return map_user(user)


def data_user_delete(user_id: int):
    user = db.session.query(User).filter_by(id=user_id).first()
    if user is not None:
        db.session.delete(user)
        db.session.commit()
