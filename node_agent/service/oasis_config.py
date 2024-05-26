import dataclasses
from datetime import date
from datetime import datetime
import json

from flask import jsonify
from node_agent.model.db import db
from node_agent.model.oasis.node import OasisNode


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, date):
            return o.isoformat()
        return super().default(o)


def export_oasis_config(json_file):
    oasis_node_list = {OasisNode.__name__: db.session.query(OasisNode).all()}

    # Write the config data to a JSON file
    with open(json_file, "w") as file:
        json.dump(
            oasis_node_list,
            file,
            cls=EnhancedJSONEncoder,
            indent=4,
        )
    return jsonify(oasis_node_list)
