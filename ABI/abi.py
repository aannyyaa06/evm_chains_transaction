import os
import json
import pandas as pd
import requests
from io import BytesIO
from tqdm import tqdm


with open("CONFIG.JSON") as f:
    config = json.load(f)

hf_config = config["huggingface_contracts"]  
token = hf_config.get("hf_token", "")
base_url = hf_config.get("base_url")
start_part = hf_config.get("start_part", 0)
end_part = hf_config.get("end_part", 1)
contracts_folder = hf_config.get("contracts_folder", "./contracts")
metadata_folder = hf_config.get("metadata_folder", "./contract_metadata")
default_contract_name = hf_config.get("default_contract_name", "UserWallet")

if not token or not token.startswith("hf_"):
    raise ValueError("Invalid or missing Hugging Face token.")

headers = {"Authorization": f"Bearer {token.strip()}"}
os.makedirs(contracts_folder, exist_ok=True)
os.makedirs(metadata_folder, exist_ok=True)

for part_num in range(start_part, end_part):
    print(f"\nProcessing part.{part_num}.parquet...")

    url = base_url.format(part_num)
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        buffer = BytesIO(response.content)
        df = pd.read_parquet(buffer)
    except Exception as e:
        print(f"Failed to download or read part.{part_num}.parquet: {e}")
        continue

    for i, row in tqdm(df.iterrows(), total=len(df), desc=f"Saving rows from part.{part_num}"):
        try:
            abi_started = False
            contract_data = []
            metadata_data = []
            contract_address = None
            contract_name = default_contract_name

            for col, val in row.items():
                val_str = "null" if pd.isnull(val) or str(val).strip() == "" else str(val)

                if col in ["library", "license_type", "implementation"] and val_str.strip() == "":
                    val_str = "null"

                if not abi_started:
                    if col == "contract_address" and val_str != "null":
                        contract_address = val_str.strip().lower()
                    if col == "contract_name" and val_str != "null":
                        contract_name = val_str.strip()

                if col.lower() == "abi":
                    abi_started = True

                (metadata_data if abi_started else contract_data).append(f"{col}: {val_str}")

            if contract_address and contract_address.startswith("0x"):
                filename_prefix = contract_address
            else:
                filename_prefix = f"unknown_row_{i}"

            contract_file = os.path.join(contracts_folder, f"{filename_prefix}_{contract_name}_userwallet.sol")
            metadata_file = os.path.join(metadata_folder, f"{filename_prefix}_address.txt")

            with open(contract_file, "w", encoding="utf-8") as f:
                f.write("\n".join(contract_data))

            with open(metadata_file, "w", encoding="utf-8") as f:
                f.write("\n".join(metadata_data))

        except Exception as row_error:
            print(f"Skipped row {i} due to error: {row_error}")
            continue

print("\nAll done. Files saved in the specified folders.")
