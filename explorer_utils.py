import requests
import time

def get_balance(address, explorer_config):
    url = explorer_config["url"]
    api_key = explorer_config["apikey"]
    params = {
        "module": "account",
        "action": "balance",
        "address": address,
        "apikey": api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data.get("result", "0")


def is_contract(address, explorer_config):
    url = explorer_config["url"]
    api_key = explorer_config["apikey"]
    params = {
        "module": "contract",
        "action": "getsourcecode",
        "address": address,
        "apikey": api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data.get("result", [{}])[0].get("ABI") != "Contract source code not verified"


def get_transactions(address, explorer_config, yield_batches=False):
    url = explorer_config.get("url") or explorer_config.get("api_url")
    api_key = explorer_config.get("apikey")

    if not url or not api_key:
        raise ValueError(f"Missing 'url' or 'apikey' in explorer_config: {explorer_config}")

    offset = 10000
    startblock = 0
    endblock = 99999999
    max_retries = 3

    all_transactions = []

    while True:
        params = {
            "module": "account",
            "action": "txlist",
            "address": address,
            "startblock": startblock,
            "endblock": endblock,
            "offset": offset,
            "sort": "asc",
            "apikey": api_key
        }

        retries = 0
        while retries < max_retries:
            try:
                response = requests.get(url, params=params, timeout=10)
                data = response.json()
                result = data.get("result")

                if result is None:
                    print(f"retry Null result, attempt {retries + 1}")
                    retries += 1
                    time.sleep(1)
                    continue

                if not isinstance(result, list):
                    print(f"error Unexpected response format: {result}")
                    return all_transactions

                if not result:
                    return all_transactions

                print(f"debug Fetched {len(result)} transactions from block {startblock}")

                if yield_batches:
                    yield result
                else:
                    all_transactions.extend(result)

                if len(result) < offset:
                    if yield_batches:
                        return 
                    return all_transactions  

                last_block = int(result[-1]["blockNumber"])
                startblock = last_block + 1
                time.sleep(0.2)
                break

            except Exception as e:
                print(f"error Failed to fetch transactions: {e}")
                return all_transactions if not yield_batches else None

        else:
            print("error Failed after retries.")
            return all_transactions if not yield_batches else None
