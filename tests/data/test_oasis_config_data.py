from node_agent.data.oasis.oasis_config_data import add_config_data


def test_add_config_data():
    with open("resources/testnet/README.md", "r") as file:
        data = file.read()
    ret = add_config_data(data)
    assert ret is not None
    assert ret["md5"] == "630b8f2150100f7f4ad50ba12723a2c2"
    assert ret["network"] == "testnet"
