# Mainnet

## Network Parameters

These are the current parameters for the Mainnet:

* [Genesis file](https://github.com/oasisprotocol/mainnet-artifacts/releases/download/2023-11-29/genesis.json):
  * SHA256: `b14e45e97da0216a16c25096fd216f591e4d526aa6abac110ac23cb327b64ba1`

:::info

Genesis file is signed by [network's current maintainers]. To verify its
authenticity, follow the [PGP verification instructions].

:::

* Genesis document's hash ([explanation](../genesis-doc.md#genesis-file-vs-genesis-document)):
  * `bb3d748def55bdfb797a2ac53ee6ee141e54cd2ab2dc2375f4a0703a178e6e55`
* Oasis seed node addresses:
  * `H6u9MtuoWRKn5DKSgarj/dzr2Z9BsjuRHgRAoXITOcU=@35.199.49.168:26656`
  * `H6u9MtuoWRKn5DKSgarj/dzr2Z9BsjuRHgRAoXITOcU=@35.199.49.168:9200`
  * `90em3ItdQkFy15GtWqCKHi5j7uEUmZPZIzBt7I5d6w4=@146.148.13.130:26656`
  * `90em3ItdQkFy15GtWqCKHi5j7uEUmZPZIzBt7I5d6w4=@146.148.13.130:9200`

:::tip

Feel free to use other seed nodes besides the one provided here.

:::

* [Oasis Core](https://github.com/oasisprotocol/oasis-core) version:
  * [23.0.11](https://github.com/oasisprotocol/oasis-core/releases/tag/v23.0.11)
* [Oasis Rosetta Gateway](https://github.com/oasisprotocol/oasis-rosetta-gateway) version:
  * [2.6.0](https://github.com/oasisprotocol/oasis-rosetta-gateway/releases/tag/v2.6.0)

:::info

The Oasis Node is part of the Oasis Core release.

:::

:::danger

Do not use a newer version of Oasis Core since it likely contains changes that
are incompatible with the version of Oasis Core used by other nodes.

:::

If you want to join our Testnet, see the [Testnet](../testnet/README.md) docs
for the current Testnet parameters.

[network's current maintainers]: https://github.com/oasisprotocol/mainnet-artifacts/blob/master/README.md#pgp-keys-of-current-maintainers
[PGP verification instructions]: https://github.com/oasisprotocol/mainnet-artifacts/blob/master/README.md#verifying-genesis-file-signatures

## ParaTimes

This section contains parameters for various ParaTimes known to be deployed on the Mainnet.

### Cipher

* Oasis Core version:
  * [23.0.11](https://github.com/oasisprotocol/oasis-core/releases/tag/v23.0.11)
* Runtime identifier:
  * `000000000000000000000000000000000000000000000000e199119c992377cb`
* Runtime bundle version:
  * [3.0.5](https://github.com/oasisprotocol/cipher-paratime/releases/tag/v3.0.5)
  * [3.0.2](https://github.com/oasisprotocol/cipher-paratime/releases/tag/v3.0.2)
* IAS proxy address:
  * `tnTwXvGbbxqlFoirBDj63xWtZHS20Lb3fCURv0YDtYw=@34.86.108.137:8650`
  * `tuDyXwaajTEbNWb1QIlf8FWHsdkaB4W1+TjzP1QID/U=@131.153.243.17:8650`

:::tip

Feel free to use other IAS proxies besides the one provided here or
[run your own](../../node/run-your-node/ias-proxy.md).

:::

### Emerald

* Oasis Core version:
  * [23.0.11](https://github.com/oasisprotocol/oasis-core/releases/tag/v23.0.11)
* Runtime identifier:
  * `000000000000000000000000000000000000000000000000e2eaa99fc008f87f`
* Runtime bundle version (or [build your own](https://github.com/oasisprotocol/emerald-paratime/tree/v11.0.0#building)):
  * [11.0.0](https://github.com/oasisprotocol/emerald-paratime/releases/tag/v11.0.0)
* Web3 Gateway version:
  * [5.0.1](https://github.com/oasisprotocol/oasis-web3-gateway/releases/tag/v5.0.1)

:::info

Check the [Emerald ParaTime page](/dapp/emerald/#rpc-endpoints) on how to access
the public Web3 endpoint.

:::

### Sapphire

* Oasis Core version:
  * [23.0.11](https://github.com/oasisprotocol/oasis-core/releases/tag/v23.0.11)
* Runtime identifier:
  * `000000000000000000000000000000000000000000000000f80306c9858e7279`
* Runtime bundle version:
  * [0.7.3](https://github.com/oasisprotocol/sapphire-paratime/releases/tag/v0.7.3)
  * [0.7.0](https://github.com/oasisprotocol/sapphire-paratime/releases/tag/v0.7.0)
* Oasis Web3 Gateway version:
  * [5.0.1](https://github.com/oasisprotocol/oasis-web3-gateway/releases/tag/v5.0.1)
* IAS proxy address:
  * `tnTwXvGbbxqlFoirBDj63xWtZHS20Lb3fCURv0YDtYw=@34.86.108.137:8650`
  * `tuDyXwaajTEbNWb1QIlf8FWHsdkaB4W1+TjzP1QID/U=@131.153.243.17:8650`

:::tip

Feel free to use other IAS proxies besides the one provided here or
[run your own](../../node/run-your-node/ias-proxy.md).

:::

### Key Manager

* Oasis Core version:
  * [23.0.11](https://github.com/oasisprotocol/oasis-core/releases/tag/v23.0.11)
* Runtime identifier:
  * `4000000000000000000000000000000000000000000000008c5ea5e49b4bc9ac`
* Runtime bundle version:
  * [0.4.1](https://github.com/oasisprotocol/keymanager-paratime/releases/tag/v0.4.1)
* IAS proxy address:
  * `tnTwXvGbbxqlFoirBDj63xWtZHS20Lb3fCURv0YDtYw=@34.86.108.137:8650`
  * `tuDyXwaajTEbNWb1QIlf8FWHsdkaB4W1+TjzP1QID/U=@131.153.243.17:8650`

:::tip

Feel free to use other IAS proxies besides the one provided here or
[run your own](../../node/run-your-node/ias-proxy.md).

:::
