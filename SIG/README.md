Created Python scripts that:
->Scrape function and event signatures (text and hex) from the 4byte.directory website.
->Store them in MongoDB, avoiding duplicates using a unique ID.
->Use a common CONFIG.JSON file and requirement.txt to manage base URLs, MongoDB details, page ranges, and delay settings.
->Add random delays between requests to avoid overwhelming the site.
