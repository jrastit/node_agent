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


def _get_version_url_list(section, i, version_list, url_list, str1, str2=None):
    if str1 in section["lines"][i] and (
        str2 == None or str2 in section["lines"][i]
    ):
        if len(version_list) > 0 or len(url_list) > 0:
            raise Exception(
                f"More than one version found for "
                + section["name"]
                + " =>"
                + str1
                + "/"
                + str2
            )
        for j in range(i + 1, len(section["lines"])):
            line = section["lines"][j]
            if len(line) == 0 or line[0] != " ":
                break
            start_index = line.find("[") + 1
            end_index = line.find("]", start_index)
            if start_index <= 0 or end_index < 0:
                break
            version_list.append(line[start_index:end_index])
            start_index = line.find("(") + 1
            end_index = line.find(")", start_index)
            if start_index <= 0 or end_index < 0:
                raise Exception("Version url not found")
            url_list.append(line[start_index:end_index])
    return version_list, url_list


def _get_oasis_core_version(section, i, version, url):
    version_list = []
    url_list = []
    if version is not None:
        version_list.append(version)
    if url is not None:
        url_list.append(url)
    version_list, url_list = _get_version_url_list(
        section,
        i,
        version_list,
        url_list,
        "Oasis Core",
        "version:",
    )
    if len(version_list) > 1 or len(url_list) > 1:
        raise Exception(
            "Oasis Core multi version not found in section " + section["name"]
        )
    elif len(version_list) == 1 and len(url_list) == 1:
        return version_list[0], url_list[0]
    return version, url


def _get_value_list(section, i, value_list, str1, str2=None):
    if (str1 in section["lines"][i]) and (
        str2 == None or (str2 in section["lines"][i])
    ):
        if len(value_list) > 0:
            raise Exception(
                f"More than one value found for "
                + section["name"]
                + " =>"
                + str1
                + "/"
                + str2
            )
        for j in range(i + 1, len(section["lines"])):
            line = section["lines"][j]
            start_index = line.find("`") + 1
            end_index = line.find("`", start_index)
            if start_index <= 0 or end_index < 0:
                break
            value_list.append(line[start_index:end_index])
    return value_list


def get_configue_from_md_file(md_file):
    with open(md_file, "r") as file:
        data = file.read()
    return get_configue_from_md(data)


def get_configue_from_md(data: str):
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
                # get genesis file
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
                # get seed node
                network_seed_node = _get_value_list(
                    section,
                    i,
                    network_seed_node,
                    "Oasis seed node addresses:",
                )
                # get core version
                network_core_version, network_core_version_url = (
                    _get_oasis_core_version(
                        section,
                        i,
                        network_core_version,
                        network_core_version_url,
                    )
                )

        elif section["name"] == "ParaTimes":

            paratime_section_list = []
            paratime_list = []
            for i in range(len(section["lines"])):
                if section["lines"][i].startswith("### "):
                    paratime_section_list.append(
                        {
                            "name": section["lines"][i][4:],
                            "lines": [],
                        }
                    )
                else:
                    if len(paratime_section_list) > 0:
                        paratime_section_list[-1]["lines"].append(
                            section["lines"][i]
                        )
            for paratime_section in paratime_section_list:
                runtime_identifier = []
                paratime = {
                    "name": paratime_section["name"],
                    "core_version": None,
                    "core_version_url": None,
                    "runtime_identifier": None,
                    "runtime_version": [],
                    "runtime_version_url": [],
                    "IAS_proxy": [],
                }
                paratime_list.append(paratime)
                for i in range(len(paratime_section["lines"])):
                    # get core version
                    paratime["core_version"], paratime["core_version_url"] = (
                        _get_oasis_core_version(
                            paratime_section,
                            i,
                            paratime["core_version"],
                            paratime["core_version_url"],
                        )
                    )
                    # get runtime identifier
                    runtime_identifier = _get_value_list(
                        paratime_section,
                        i,
                        runtime_identifier,
                        "Runtime identifier",
                    )
                    # get runtime version
                    (
                        paratime["runtime_version"],
                        paratime["runtime_version_url"],
                    ) = _get_version_url_list(
                        paratime_section,
                        i,
                        paratime["runtime_version"],
                        paratime["runtime_version_url"],
                        "Runtime bundle version",
                    )
                    # get IAS proxy
                    paratime["IAS_proxy"] = _get_value_list(
                        paratime_section,
                        i,
                        paratime["IAS_proxy"],
                        "IAS proxy",
                    )
                if len(runtime_identifier) > 1:
                    raise Exception(
                        "More than one runtime identifier found in section "
                        + paratime_section["name"]
                    )
                elif len(runtime_identifier) == 1:
                    paratime["runtime_identifier"] = runtime_identifier[0]

    return {
        "network": network,
        "network_genesis_file": network_genesis_file,
        "network_seed_node": network_seed_node,
        "network_core_version": network_core_version,
        "network_core_version_url": network_core_version_url,
        "paratime_list": paratime_list,
    }
