<div align="center">

# ⛓️ EVM Chains Transaction Fetcher

### Multi-Chain Blockchain Data Collection & Storage Pipeline

**27 EVM Chains · 80,000+ Transactions · MongoDB Storage**

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Database-47A248?style=flat-square&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Ethereum](https://img.shields.io/badge/EVM-Compatible-627EEA?style=flat-square&logo=ethereum&logoColor=white)](https://ethereum.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

---

## Overview

I built this tool because pulling transaction data across multiple EVM chains manually is genuinely painful — different explorers, different API quirks, inconsistent responses. This project wraps all of that into a single, clean pipeline.

Point it at a list of wallet addresses, configure your API keys once, and it handles the rest — fetching transaction history, checking balances, and figuring out whether each address is a smart contract or a regular wallet. Everything lands in MongoDB so you can actually query and work with the data.

It currently supports **27 EVM-compatible blockchains** and can handle **80,000+ transactions per address** without breaking a sweat.

What it fetches for each address:
- 📜 **Transaction History** — full history, paginated automatically
- 💰 **Wallet Balances** — current native token balance per chain
- 🔍 **Contract Detection** — tells you if it's a smart contract (CA) or a regular wallet (EOA)

---

## What It Does Well

| | |
|---|---|
|  27 Chains | Covers all major EVM networks in one run |
|  Big datasets | Tested with 80,000+ transactions per address — no issues |
|  Knows the difference | Automatically flags smart contracts vs. regular wallets |
|  Stays organized | Drops everything into MongoDB so you can query it later |
|  Easy to configure | One JSON file to rule all your API keys and endpoints |
|  Easy to extend | Adding a new chain takes literally 4 lines in `CONFIG.JSON` |

---

## Project Structure

```
evm_chains_transaction_fetcher/
│
├── main1.py               # Main orchestration script
├── explorer_utils.py      # Blockchain explorer API helpers
├── CONFIG.JSON            # API keys, base URLs, and settings
├── address1.txt           # Input: wallet addresses to process
│
├── ABI/                   # Subproject: Smart contract code downloader
│   └── ...
│
└── SIG/                   # Subproject: Function/event signature scraper
    └── ...
```

---

## Core Components

### `main1.py`
This is where everything kicks off. It reads your address list, loops through each chain, fetches the data, and writes it all to MongoDB. Run this when you're ready to collect.

### `explorer_utils.py`
All the messy API stuff lives here — pagination, rate-limit handling, response parsing, and dealing with the quirks of each explorer's API. You probably won't need to touch this often.

### `CONFIG.JSON`
The only file you really need to edit before running. Put your API keys and MongoDB connection string here and you're good to go.

```json
{
  "chains": [
    {
      "name": "Ethereum",
      "base_url": "https://api.etherscan.io/api",
      "api_key": "YOUR_API_KEY"
    }
  ],
  "mongodb_uri": "mongodb://localhost:27017",
  "database": "blockchain_data"
}
```

### `address1.txt`
Plain-text list of wallet addresses to process — one address per line.

```
0xAbCd...1234
0xEfGh...5678
```

---

## Subprojects

These are two standalone utilities that live alongside the main tool.

### 📁 `ABI/` — Smart Contract Code Collector

Pulls verified smart contract source code from Hugging Face and splits the output into `.sol` and `.txt` files. Handy if you're doing contract analysis or building a local reference dataset.

### 📁 `SIG/` — Function & Event Signature Scraper

Scrapes function and event signatures from [4byte.directory](https://www.4byte.directory/) and converts them into their 4-byte hex selectors. Results go straight into MongoDB. Useful for decoding calldata or building a local signature lookup.

---

## Getting Started

You'll need Python 3.x, a running MongoDB instance (local or Atlas), and API keys from whichever explorer APIs you plan to hit.

### Setup

```bash
# Clone and enter the project
git clone https://github.com/your-username/evm_chains_transaction_fetcher.git
cd evm_chains_transaction_fetcher

# Install dependencies
pip install -r requirements.txt
```

### Running It

```bash
# 1. Drop your wallet addresses into address1.txt — one per line
nano address1.txt

# 2. Add your API keys and MongoDB URI to CONFIG.JSON
nano CONFIG.JSON

# 3. Fire it up
python main1.py

# 4. Check your results in MongoDB
mongosh
> use blockchain_data
> db.transactions.find({ address: "0xAbCd...1234" })
```

That's it. The script handles pagination, rate limits, and retries automatically.

---

## MongoDB Output

Every document in the collection includes the wallet address, chain name, full transaction list, current balance, and whether the address is a contract or EOA.

<img width="1265" height="1017" alt="image" src="https://github.com/user-attachments/assets/bd8b4bf1-a5b0-4f47-8b2d-6dcab58cb6b1" />

---

## Supported Blockchains

27 EVM-compatible chains are supported out of the box:

| # | Network | Explorer | API Key |
|---|---|---|---|
| 1 | Ethereum (ETH) | [etherscan.io](https://etherscan.io/) |  Required |
| 2 | BNB Smart Chain | [bscscan.com](https://bscscan.com/) |  Required |
| 3 | Polygon (MATIC) | [polygonscan.com](https://polygonscan.com/) | Required |
| 4 | Arbitrum | [arbiscan.io](https://arbiscan.io/) | Required |
| 5 | Optimism | [optimistic.etherscan.io](https://optimistic.etherscan.io/) | Required |
| 6 | Fantom (FTM) | [explorer.fantom.network](https://explorer.fantom.network/) | Required |
| 7 | Avalanche (AVAX) | [snowtrace.io](https://snowtrace.io/) | Required |
| 8 | Moonbeam | [moonscan.io](https://moonscan.io/) | Required |
| 9 | Linea | [lineascan.build](https://lineascan.build/) |  Required |
| 10 | Base | [basescan.org](https://basescan.org/) |  Required |
| 11 | zkSync Era | [explorer.zksync.io](https://explorer.zksync.io/) |  Required |
| 12 | Scroll | [scrollscan.com](https://scrollscan.com/) |  Required |
| 13 | Blast | [blastscan.io](https://blastscan.io/) | Required |
| 14 | Gnosis Chain | [gnosisscan.io](https://gnosisscan.io/) | Required |
| 15 | Cronos | [cronoscan.com](https://cronoscan.com/) |  Required |
| 16 | HECO Chain | [hecoinfo.com](https://hecoinfo.com/) | Required |
| 17 | Astar | [astar.subscan.io](https://astar.subscan.io/) | Required |
| 18 | Mantle | [mantlescan.xyz](https://mantlescan.xyz/) |  Required |
| 19 | Celo | [celoscan.io](https://celoscan.io/) |  Required |
| 20 | Core | [corescan.io](https://corescan.io/) |  Required |
| 21 | KuCoin Community Chain | [explorer.kcc.io](https://explorer.kcc.io/) |  Required |
| 22 | Telos | [teloscan.io](https://teloscan.io/) |  Required |
| 23 | Aurora | [aurorascan.dev](https://aurorascan.dev/) |  Required |
| 24 | Meter | [scan.meter.io](https://scan.meter.io/) |  Required |
| 25 | Harmony | [explorer.harmony.one](https://explorer.harmony.one/) |  Required |
| 26 | Evmos | [atomscan.com/evmos](https://atomscan.com/evmos) |  Required |
| 27 | Fuse | [explorer.fuse.io](https://explorer.fuse.io/) |  Required |

> ℹ️ To add a new chain, simply append its configuration to `CONFIG.JSON` — no code changes required.

---

## Adding a New Chain

If the chain has an Etherscan-compatible API (most do), adding it takes about 30 seconds:

1. Grab an API key from the chain's explorer
2. Add this to `CONFIG.JSON`:

```json
{
  "name": "NewChain",
  "base_url": "https://api.newchain-explorer.io/api",
  "api_key": "YOUR_KEY_HERE"
}
```

3. Re-run `main1.py` — it picks up the new chain automatically.

---

## License

MIT — use it however you like. See [LICENSE](LICENSE) for the details.

---

<div align="center">

Built for on-chain analysts and blockchain data engineers · **27 chains and counting**

</div>



