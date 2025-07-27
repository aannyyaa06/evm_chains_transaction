import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient, errors
import time
import json
import random


with open("./CONFIG.JSON") as f:
    config = json.load(f)


fourbyte_config = config["fourbyte"]
event_config = fourbyte_config["event_signatures"]


client = MongoClient(fourbyte_config["mongodb_uri"])
db = client[fourbyte_config["database"]]
collection = db[event_config["collection"]]

def scrape_event_page(page_number):
    url = f"{event_config['base_url']}{page_number}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table")
    if not table:
        print(f"No table found on page {page_number}")
        return

    rows = table.find_all("tr")[1:]
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 3:
            try:
                id_value = int(cols[0].text.strip())
                signature = cols[1].text.strip()
                hex_signature = cols[2].text.strip()

                data = {
                    "_id": id_value,
                    "signature": signature,
                    "hex_signature": hex_signature
                }

                collection.insert_one(data)
                print(f"Inserted: {data}")
            except errors.DuplicateKeyError:
                print(f"Duplicate: ID {id_value} already exists.")
            except Exception as e:
                print(f"Error on ID {id_value}: {e}")


for page in range(event_config["start_page"], event_config["end_page"] + 1):
    print(f"\nScraping event signature page {page}/{event_config['end_page']}")
    scrape_event_page(page)
    delay = random.uniform(*event_config["delay_range"])
    print(f"Sleeping for {delay:.2f} seconds...")
    time.sleep(delay)
