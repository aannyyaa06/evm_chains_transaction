import os
import json
from pymongo import MongoClient
from datetime import datetime, timezone
from explorer_utils import get_balance, is_contract, get_transactions


with open(os.path.join(os.path.dirname(__file__), "CONFIG.json")) as f:
    CONFIG = json.load(f)

MONGO = CONFIG["mongodb"]
client = MongoClient(MONGO["uri"])

all_explorers = CONFIG["explorers"]

def load_addresses_from_file(filename="address1.txt"):
    try:
        with open(filename, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[ERROR] File not found: {filename}")
        return []

def wei_to_eth(wei):
    try:
        return int(wei) / 1e18
    except Exception:
        return 0

def is_valid_api_key(key):
    invalid_placeholders = {"", "your_api_key_here", "<your_api_key_here>"}
    return key and key.strip().lower() not in invalid_placeholders

def fetch_and_store_all_data():
    valid_explorers = {
        name: exp for name, exp in all_explorers.items()
        if is_valid_api_key(exp.get("apikey", ""))
    }

    addresses = load_addresses_from_file()
    if not addresses:
        print(" No addresses loaded. Exiting.")
        return

    if not valid_explorers:
        print("No valid explorers configured with API keys.")
        return

    print(f"Using explorers: {[exp['name'] for exp in valid_explorers.values()]}")
    print(f"Total addresses loaded: {len(addresses)}")

    for address in addresses:
        print(f"\n Processing address: {address}")
        for explorer_name, explorer_config in valid_explorers.items():
            chain_name = explorer_config["name"]
            print(f" Using Explorer: {chain_name}")

            try:
                collection_base = explorer_name.strip().lower()
                tx_collection = client[MONGO["target_db"]][f"{collection_base}_transaction"]
                meta_collection = client[MONGO["target_db"]][f"{collection_base}_metadata"]

                tx_collection.delete_many({"address": address, "explorer_used": chain_name})
                total_saved = 0

                for batch in get_transactions(address, explorer_config, yield_batches=True):
                    if not isinstance(batch, list):
                        print(f" Invalid batch format received: {batch}")
                        continue

                    docs = []
                    for tx in batch:
                        if not isinstance(tx, dict):
                            print(f" Invalid transaction format: {tx}")
                            continue

                        docs.append({
                            "address": address,
                            "explorer_used": chain_name,
                            "hash": tx.get("hash"),
                            "from_address": tx.get("from"),
                            "to_address": tx.get("to"),
                            "value": str(wei_to_eth(tx.get("value"))),
                            "block_number": tx.get("blockNumber"),
                            "block_hash": tx.get("blockHash"),
                            "gas": tx.get("gas"),
                            "gas_price": tx.get("gasPrice"),
                            "nonce": tx.get("nonce"),
                            "input": tx.get("input"),
                            "transaction_index": tx.get("transactionIndex"),
                            "transaction_type": tx.get("type"),
                            "gas_used": tx.get("gasUsed"),
                            "status": tx.get("txreceipt_status"),
                            "block_timestamp": tx.get("timeStamp"),
                        })

                    if docs:
                        tx_collection.insert_many(docs)
                        total_saved += len(docs)
                        print(f"  saved {len(docs)} transactions (Total: {total_saved})")

                meta_doc = {
                    "address": address,
                    "explorer_used": chain_name,
                    "timestamp": datetime.now(timezone.utc),
                    "balance": get_balance(address, explorer_config),
                    "is_contract": is_contract(address, explorer_config)
                }

                meta_collection.update_one(
                    {"address": address},
                    {"$set": meta_doc},
                    upsert=True
                )

                print(f"  Stored metadata for {address}")

            except Exception as e:
                print(f" Failed processing {address} on {chain_name}: {e}")

if __name__ == "__main__":
    fetch_and_store_all_data()
