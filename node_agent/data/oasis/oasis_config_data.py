import hashlib
import logging

from node_agent.model.db import db

from node_agent.model.oasis.config import OasisConfig, OasisParatimeConfig
from node_agent.service.oasis.oasis_config import get_configue_from_md

logger = logging.getLogger()


def map_config_data(oasis_config_db, paratime_list_db=None):
    oasis_config = {
        "id": oasis_config_db.id,
        "time_create": oasis_config_db.time_create,
        "time_updated": oasis_config_db.time_updated,
        "md5": oasis_config_db.md5,
        "network": oasis_config_db.network,
        "network_genesis_file": oasis_config_db.network_genesis_file,
        "network_seed_node": oasis_config_db.network_seed_node,
        "network_core_version": oasis_config_db.network_core_version,
        "network_core_version_url": oasis_config_db.network_core_version_url,
        "validate": oasis_config_db.validate,
        "paratime": [],
    }
    for paratime in oasis_config_db.oasis_config_paratime:
        oasis_config_paratime = map_paratime_data(paratime)
        oasis_config["paratime"].append(oasis_config_paratime)

    return oasis_config


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
    db.session.commit()
    for paratime in config["paratime_list"]:
        paratime_config_db = OasisParatimeConfig(
            name=paratime["name"],
            core_version=paratime["core_version"],
            core_version_url=paratime["core_version_url"],
            runtime_identifier=paratime["runtime_identifier"],
            runtime_version=paratime["runtime_version"],
            runtime_version_url=paratime["runtime_version_url"],
            IAS_proxy=paratime["IAS_proxy"],
            oasis_config=oasis_config_db,
        )
        db.session.add(paratime_config_db)
    db.session.commit()
    oasis_config = map_config_data(oasis_config_db)
    return oasis_config


def get_last_config_data(network, validate=True):
    oasis_config_db = (
        db.session.query(OasisConfig)
        .filter(
            OasisConfig.validate == validate, OasisConfig.network == network
        )
        .order_by(OasisConfig.id.desc())
        .first()
    )
    if oasis_config_db is None:
        return None
    oasis_config_paratime_db = (
        db.session.query(OasisParatimeConfig)
        .filter(OasisParatimeConfig.oasis_config_id == oasis_config_db.id)
        .all()
    )
    return map_config_data(
        oasis_config_db, paratime_list_db=oasis_config_paratime_db
    )
