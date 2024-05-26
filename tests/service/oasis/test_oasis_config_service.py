from node_agent.service.oasis.oasis_config import get_configue_from_md_file


def test_get_md_values():
    ret = get_configue_from_md_file("resources/mainnet/README.md")
    assert ret is not None
    assert "network" in ret
    assert "network_genesis_file" in ret
    assert "network_seed_node" in ret
    assert "network_core_version" in ret
    assert "network_core_version_url" in ret
    assert ret["network"] == "mainnet"
    assert (
        ret["network_genesis_file"]
        == "https://github.com/oasisprotocol/mainnet-artifacts/releases/download/2023-11-29/genesis.json"
    )
    assert len(ret["network_seed_node"]) > 0
    assert (
        ret["network_seed_node"][0]
        == "H6u9MtuoWRKn5DKSgarj/dzr2Z9BsjuRHgRAoXITOcU=@35.199.49.168:26656"
    )
    assert ret["network_core_version"] == "23.0.11"
    assert (
        ret["network_core_version_url"]
        == "https://github.com/oasisprotocol/oasis-core/releases/tag/v23.0.11"
    )

    ret = get_configue_from_md_file("resources/testnet/README.md")
    assert ret is not None
    assert "network" in ret
    assert "network_genesis_file" in ret
    assert "network_seed_node" in ret
    assert "network_core_version" in ret
    assert "network_core_version_url" in ret
    assert ret["network"] == "testnet"
    assert (
        ret["network_genesis_file"]
        == "https://github.com/oasisprotocol/testnet-artifacts/releases/download/2023-10-12/genesis.json"
    )
    assert len(ret["network_seed_node"]) > 0
    assert (
        ret["network_seed_node"][0]
        == "HcDFrTp/MqRHtju5bCx6TIhIMd6X/0ZQ3lUG73q5898=@34.86.165.6:26656"
    )
    assert ret["network_core_version"] == "24.0"
    assert (
        ret["network_core_version_url"]
        == "https://github.com/oasisprotocol/oasis-core/releases/tag/v24.0"
    )
