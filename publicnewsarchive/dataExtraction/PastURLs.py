import requests
from requests.exceptions import Timeout
def getPastURLs(year, newspaper_url, startMonth='01', endMonth='12'):

    url_api = 'https://arquivo.pt/textsearch'

    versionHistory = newspaper_url
    maxItems = '5000'
    fromDate = f'{year}{startMonth}01000000'
    toDate = f'{year}{endMonth}31235959'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Referer': 'https://www.google.com'
}
    payload = {'versionHistory': versionHistory, 'maxItems': maxItems, 'from': fromDate, 'to': toDate,}
    mime ="text/html"
    status = 200

    try:
        r = requests.get(url_api, params=payload, headers=headers, timeout=60)
    except Timeout:
        print('Timeout has been raised.')


    content = r.json()
    
    pastURLs = []

    for item in content['response_items']:
        #Check for status and mime vars
        if item['statusCode'] == status and item['mimeType'] == mime:
            pastURLs.append(item['linkToNoFrame'])

    return list(set(pastURLs))