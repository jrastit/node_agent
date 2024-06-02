import logging

from node_agent.data.oasis.oasis_config_data import (
    add_config_data,
    get_last_config_data,
)

logger = logging.getLogger()


def test_add_config_data():
    with open("resources/testnet/README.md", "r") as file:
        data = file.read()
    ret = add_config_data(data)
    assert ret is not None
    assert ret["md5"] == "630b8f2150100f7f4ad50ba12723a2c2"
    assert ret["network"] == "testnet"
    assert len(ret["paratime"]) == 4

    oasis_config = get_last_config_data(ret["network"], None)
    assert oasis_config is not None
    assert oasis_config["md5"] == "630b8f2150100f7f4ad50ba12723a2c2"
    assert oasis_config["network"] == "testnet"
    assert oasis_config["network_genesis_file"] is not None
    assert oasis_config["network_seed_node"] is not None
    assert oasis_config["network_core_version"] is not None
    assert oasis_config["network_core_version_url"] is not None

    assert len(oasis_config["paratime"]) == 4
    for paratime in oasis_config["paratime"]:
        assert paratime["name"] is not None
        assert paratime["core_version"] is not None
        assert paratime["core_version_url"] is not None
        assert paratime["runtime_identifier"] is not None
        assert paratime["runtime_version"] is not None
        assert paratime["runtime_version_url"] is not None
        assert paratime["IAS_proxy"] is not None
        assert paratime["oasis_config_id"] == oasis_config["id"]
