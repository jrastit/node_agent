from node_agent.model.db import db
from sqlalchemy import text


def oasis_node_data_update_nodetype(node, data):
    nodetype_list = []
    for nodetype in node.nodetype:
        nodetype_list.append(nodetype.id)
    if "nodetype_id" in data:
        for nodetype_id in data["nodetype_id"]:
            if nodetype_id not in nodetype_list:
                db.session.execute(
                    text(
                        f"INSERT INTO oasis_node_nodetype (node_id, nodetype_id) VALUES ({node.id}, {nodetype_id})"
                    )
                )
            else:
                nodetype_list.remove(nodetype_id)
    for nodetype_id in nodetype_list:
        db.session.execute(
            text(
                f"DELETE FROM oasis_node_nodetype WHERE node_id={node.id} AND nodetype_id={nodetype_id}"
            )
        )
    db.session.commit()
