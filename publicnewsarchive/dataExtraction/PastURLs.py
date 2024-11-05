import requests
import json
from requests.exceptions import Timeout

def getPastURLs(year, newspaper_url, startMonth='01', endMonth='12'):
    url_api = 'https://arquivo.pt/textsearch'

    versionHistory = newspaper_url
    maxItems = 5000
    fromDate = f'{year}{startMonth}01000000'
    toDate = f'{year}{endMonth}31235959'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://www.google.com'
    }
    payload = {
        'versionHistory': versionHistory,
        'maxItems': str(maxItems),
        'from': fromDate,
        'to': toDate,
    }
    mime = "text/html"
    status = 200

    try:
        r = requests.get(url_api, params=payload, headers=headers, timeout=600)
    except Timeout:
        print(f'Timeout has been raised, status code: N/A')
        return []

    content = r.json()
    pastURLs = []
    skippedItems = []  # List to store skipped items

    for item in content.get('response_items', []):
        # Check for the existence of statusCode and mimeType before accessing
        if 'statusCode' in item and 'mimeType' in item:
            if item['statusCode'] == status and item['mimeType'] == mime:
                pastURLs.append(item['linkToNoFrame'])
            else:
                skippedItems.append(item)  # Store the skipped item
        else:
            skippedItems.append(item)  # Store the skipped item

    print(f"Finished processing. Total URLs found: {len(pastURLs)}, Estimated URLs: {content.get('estimated_nr_results', 'N/A')}")

    # Save past URLs to a JSON file
    path = "data/"
    past_urls_filename = f'past_urls_{year}.json'
    with open(f'{path + past_urls_filename}', 'w', encoding='utf-8') as fp:
        json.dump(pastURLs, fp, ensure_ascii=False, indent=4)

    # Save skipped items to a JSON file
    if skippedItems:
        skipped_filename = f'skipped_items_{year}.json'
        with open(f'{path + skipped_filename}', 'w', encoding='utf-8') as fp:
            json.dump(skippedItems, fp, ensure_ascii=False, indent=4)

    return pastURLs
