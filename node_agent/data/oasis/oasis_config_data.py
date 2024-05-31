import hashlib

from node_agent.model.db import db

from node_agent.model.oasis.config import OasisConfig, OasisParatimeConfig
from node_agent.service.oasis.oasis_config import get_configue_from_md


def map_config_data(record):
    return {
        "id": record.id,
        "time_create": record.time_create,
        "time_updated": record.time_updated,
        "md5": record.md5,
        "network": record.network,
        "network_genesis_file": record.network_genesis_file,
        "network_seed_node": record.network_seed_node,
        "network_core_version": record.network_core_version,
        "network_core_version_url": record.network_core_version_url,
        "validate": record.validate,
        "paratime": [],
    }


def map_paratime_data(record):
    return {
        "id": record.id,
        "time_create": record.time_create,
        "time_updated": record.time_updated,
        "name": record.name,
        "core_version": record.core_version,
        "core_version_url": record.core_version_url,
        "runtime_identifier": record.runtime_identifier,
        "runtime_version": record.runtime_version,
        "runtime_version_url": record.runtime_version_url,
        "IAS_proxy": record.IAS_proxy,
        "oasis_config_id": record.oasis_config_id,
    }


def add_config_data(data, force=False):
    md5 = hashlib.md5(data.encode()).hexdigest()
    oasis_config_db = db.session.query(OasisConfig).filter_by(md5=md5).first()
    if oasis_config_db is not None and not force:
        oasis_config_db.save()
        return oasis_config_db
    config = get_configue_from_md(data)
    oasis_config_db = OasisConfig(
        md5=md5,
        network=config["network"],
        network_genesis_file=config["network_genesis_file"],
        network_seed_node=config["network_seed_node"],
        network_core_version=config["network_core_version"],
        network_core_version_url=config["network_core_version_url"],
    )
    db.session.add(oasis_config_db)
    oasis_config = map_config_data(oasis_config_db)
    for paratime in config["paratime_list"]:
        paratime_config_db = OasisParatimeConfig(
            name=paratime["name"],
            core_version=paratime["core_version"],
            core_version_url=paratime["core_version_url"],
            runtime_identifier=paratime["runtime_identifier"],
            runtime_version=paratime["runtime_version"],
            runtime_version_url=paratime["runtime_version_url"],
            IAS_proxy=paratime["IAS_proxy"],
            oasis_config_id=oasis_config_db.id,
        )
        db.session.add(paratime_config_db)
        oasis_config_paratim = map_paratime_data(paratime_config_db)
        oasis_config["paratime"].append(oasis_config_paratim)
    db.session.commit()
    return oasis_config
