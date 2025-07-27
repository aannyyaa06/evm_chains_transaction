# evm_chains_transaction_fetcher

This project collects and stores data related to blockchain wallets across 27 EVM-compatible chains. It reads wallet addresses from a file and uses blockchain explorer APIs (such as Etherscan, Polygonscan, Snowtrace, etc.) to fetch:

- Transaction history (supports 80,000+ transactions per address)
- Current wallet balance
- Contract status (whether the address is a smart contract or an externally owned account)

All collected data is processed and stored in a MongoDB database for efficient querying and analysis.

The tool supports multiple explorers by configuring valid API keys and base URLs in a JSON configuration file.

## Key Features

- Works with 27 EVM-compatible blockchains
- Handles large datasets (80,000+ transactions per address)
- Identifies contract vs. wallet addresses
- Stores structured data in MongoDB
- Configurable and extendable via JSON-based settings
---
## Key Components

- **main1.py**  
  Main script that runs the data collection and processing logic.

- **explorer_utils.py**  
  Contains helper functions for interacting with blockchain explorer APIs.

- **CONFIG.JSON**  
  Stores all API keys, explorer endpoints, and other settings needed for the tool to operate.

- **address1.txt**  
  A text file listing wallet addresses to be processed.

---
## Requirements

- Python 3.x
- MongoDB
- Valid API keys for the targeted blockchain explorers (e.g., Etherscan, Polygonscan)

---

## How to Use

1. Add wallet addresses to `address1.txt`.
2. Configure API keys and explorer URLs in `CONFIG.JSON`.
3. Run `main1.py` to start data collection.
4. Use MongoDB tools or scripts to analyze stored data.

---
## Output saved in mongo db
<br>

![Screenshot 2025-06-26 011342](https://github.com/user-attachments/assets/a624f34b-8a81-4716-b496-dde43cffc03b)

<br>

# Blockchain Explorer API Reference

Below is a list of blockchain networks and their respective block explorers, including whether an API key is required.

| **Blockchain Network**                  | **Explorer Name**       | **Explorer URL**                                  | **API Key Required?** |
|----------------------------------------|--------------------------|---------------------------------------------------|------------------------|
| Ethereum (ETH)                         | Etherscan               | [etherscan.io](https://etherscan.io/)             | Yes                    |
| BNB Smart Chain (BNB)                  | BscScan                 | [bscscan.com](https://bscscan.com/)               | Yes                    |
| Polygon (MATIC)                        | PolygonScan             | [polygonscan.com](https://polygonscan.com/)       | Yes                    |
| Arbitrum                               | Arbiscan                | [arbiscan.io](https://arbiscan.io/)               | Yes                    |
| Optimism                               | Optimistic Etherscan    | [optimistic.etherscan.io](https://optimistic.etherscan.io/) | Yes          |
| Fantom (FTM)                           | FTMScan                 | https://explorer.fantom.network/                                  | Yes                    |
| Avalanche (AVAX)                       | SnowTrace               | [snowtrace.io](https://snowtrace.io/)             | Yes                    |
| Moonbeam                               | MoonScan                | [moonscan.io](https://moonscan.io/)               | Yes                    |
| Linea                                  | LineaScan               | [lineascan.build](https://lineascan.build/)       | Yes                    |
| Base                                   | BaseScan                | [basescan.org](https://basescan.org/)             | Yes                    |
| zkSync Era                             | zkSync Explorer         | [explorer.zksync.io](https://explorer.zksync.io/) | Yes                    |
| Scroll                                 | ScrollScan              | [scrollscan.com](https://scrollscan.com/)         | Yes                    |
| Blast                                  | Blastscan               | [blastscan.io](https://blastscan.io/)             | Yes                    |
| Gnosis Chain                           | Gnosisscan              | [gnosisscan.io](https://gnosisscan.io/)           | Yes                    |
| Cronos                                 | CronoScan               | [cronoscan.com](https://cronoscan.com/)           | Yes                    |
| HECO Chain                             | HecoInfo                | [hecoinfo.com](https://hecoinfo.com/)             | Yes                    |
| Astar                                  | AstarScan               | https://astar.subscan.io/                                   | Yes                    |
| Mantle                                 | MantleScan              | [mantlescan.xyz](https://mantlescan.xyz/)         | Yes                    |
| Celo                                   | Celo Explorer           | [celoscan.io](https://celoscan.io/)               | Yes                    |
| Core                                   | CoreScan                | [corescan.io](https://corescan.io/)               | Yes                    |
| KuCoin Community Chain (KCC)           | KCC Explorer            | [explorer.kcc.io](https://explorer.kcc.io/)       | Yes                    |
| Telos                                  | Teloscan                | [teloscan.io](https://teloscan.io/)               | Yes                    |
| Aurora                                 | AuroraScan              | [aurorascan.dev](https://aurorascan.dev/)         | Yes                    |
| Meter                                  | MeterScan               | [scan.meter.io](https://scan.meter.io/)           | Yes                    |
| Harmony                                | Harmony Explorer        | [explorer.harmony.one](https://explorer.harmony.one/) | Yes               |
| Evmos                                  | Evmos Explorer          | https://atomscan.com/evmos                                 | Yes                    |
| Fuse                                   | Fuse Explorer           | [explorer.fuse.io](https://explorer.fuse.io/)     | Yes                    |






