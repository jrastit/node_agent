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


def get_confile_from_md_file(md_file):
    with open(md_file, "r") as file:
        data = file.read()
    return get_confile_from_md(data)


def get_confile_from_md(data: str):
    network = None
    network_genesis_file = None
    network_seed_node = []
    network_core_version = None
    network_core_version_url = None

    section_list = []

    lines = data.splitlines()
    for i in range(len(lines)):
        if lines[i].startswith("# "):
            if network is not None:
                raise Exception("More than one network found")
            network = lines[i][2:].lower()
    for i in range(len(lines)):
        if lines[i].startswith("## "):
            section_list.append(
                {
                    "name": lines[i][3:],
                    "lines": [],
                }
            )
        else:
            if len(section_list) > 0:
                section_list[-1]["lines"].append(lines[i])
            elif network == "testnet":
                section_list.append(
                    {
                        "name": "Network Parameters",
                        "lines": [lines[i]],
                    }
                )
    for section in section_list:
        if section["name"] == "Network Parameters":
            for i in range(len(section["lines"])):
                if "[Genesis file]" in section["lines"][i]:
                    if network_genesis_file is not None:
                        raise Exception("More than one genesis file found")
                    line = section["lines"][i]
                    start_index = line.find("(") + 1
                    if start_index <= 0:
                        raise Exception("Genesis file not found")
                    end_index = line.find(")", start_index)
                    if end_index < 0:
                        raise Exception("Genesis end file not found")
                    network_genesis_file = line[start_index:end_index]
                if "Oasis seed node addresses:" in section["lines"][i]:
                    if len(network_seed_node) > 0:
                        raise Exception(
                            "More than one seed node section found"
                        )
                    for j in range(i + 1, len(section["lines"])):
                        line = section["lines"][j]
                        start_index = line.find("`") + 1
                        if start_index <= 0:
                            break
                        end_index = line.find("`", start_index)
                        if end_index < 0:
                            raise Exception(
                                f"Seed node address not found in line {line} {start_index} {end_index}"
                            )
                        network_seed_node.append(line[start_index:end_index])
                if (
                    "[Oasis Core]" in section["lines"][i]
                    and "version:" in section["lines"][i]
                ):
                    if (
                        network_core_version is not None
                        or network_core_version_url is not None
                    ):
                        raise Exception(
                            "More than one Oasis Core version found"
                        )
                    line = section["lines"][i + 1]
                    start_index = line.find("[") + 1
                    end_index = line.find("]", start_index)
                    if start_index <= 0 or end_index < 0:
                        raise Exception("Oasis Core version not found")
                    network_core_version = line[start_index:end_index]
                    start_index = line.find("(") + 1
                    end_index = line.find(")", start_index)
                    if start_index <= 0 or end_index < 0:
                        raise Exception("Oasis Core version url not found")
                    network_core_version_url = line[start_index:end_index]
        else:
            print(f"Section '{section['name']}' not found")

    return {
        "network": network,
        "network_genesis_file": network_genesis_file,
        "network_seed_node": network_seed_node,
        "network_core_version": network_core_version,
        "network_core_version_url": network_core_version_url,
    }
