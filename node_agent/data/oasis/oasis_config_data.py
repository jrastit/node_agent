import hashlib

from node_agent.model.oasis.config import OasisConfig, OasisParatimeConfig
from node_agent.service.oasis.oasis_config import get_configue_from_md


def add_config_data(data, force=False):
    md5 = hashlib.md5(data).hexdigest()
    record = OasisConfig.query.filter_by(md5=md5).first()
    if record is not None and not force:
        return record
    config = get_configue_from_md(data)
    record = OasisConfig(
        md5=md5,
        network=config["network"],
        network_genesis_file=config["network_genesis_file"],
        network_seed_node=config["network_seed_node"],
        network_core_version=config["network_core_version"],
        network_core_version_url=config["network_core_version_url"],
    )
    record.save()
    for paratime in config["paratime"]:
        paratime_record = OasisParatimeConfig(
            name=paratime["name"],
            core_version=paratime["core_version"],
            core_version_url=paratime["core_version_url"],
            runtime_identifier=paratime["runtime_identifier"],
            runtime_version=paratime["runtime_version"],
            runtime_version_url=paratime["runtime_version_url"],
            IAS_proxy=paratime["IAS_proxy"],
            oasis_config_id=record.id,
        )
        paratime_record.save()
    return record
