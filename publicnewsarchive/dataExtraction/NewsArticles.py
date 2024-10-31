import requests
from bs4 import BeautifulSoup
import json
import os
def getNewsArticles(pastURLs, news_htmlTag, news_htmlClass, links_htmlTag, links_htmlClass, filename, debug=False):
    
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Referer': 'https://www.google.com'
}
    journalurl = pastURLs[0]
    journalurl_slash_index = pastURLs[0].rfind('/https')
    journalurl = journalurl[journalurl_slash_index + 1:]


    dictOfTags = {'Link': [links_htmlTag, links_htmlClass]}

    ListOfContents = []
    ListOfBadContents = []
    ListOfProcessedLinks = []


    for i in range(len(pastURLs)):
        page = requests.get(pastURLs[i])
        soup = BeautifulSoup(page.content, 'html.parser', from_encoding="UTF-8")
        ListOfTagContents = soup.find_all(news_htmlTag, class_=news_htmlClass)
        print(f"Found {len(ListOfTagContents)} articles on page: {pastURLs[i]}")

        for content in ListOfTagContents:
            dictOfFeatures = {}
            dictOfFeatures['JournalURL'] = journalurl
            for key in dictOfTags:
                try:
                    if key == "Link":
                        link = content.find(dictOfTags[key][0], class_=dictOfTags[key][1]).get("href").strip()
                        if link.startswith('/noFrame/replay/'):
                            link = link.replace('/noFrame/replay/', 'https://arquivo.pt/noFrame/replay/')
                        dictOfFeatures[key] = link
                    else:
                        dictOfFeatures[key] = content.find(dictOfTags[key][0], class_=dictOfTags[key][1]).get_text().strip()
                except:
                    dictOfFeatures[key] = ' '

            try: 
                response = requests.get(link, headers=headers, timeout=10)
                if response.status_code == 200 and link not in ListOfProcessedLinks:
                    dictOfFeatures[key] = link
                    ListOfProcessedLinks.append(link)
                    ListOfContents.append(dictOfFeatures)
                else: 
                    last_slash_index = link.rfind('/https')
                    link = link[last_slash_index + 1:]
                    dictOfFeatures[key] = link
                    try: 
                        response = requests.get(link, headers=headers, timeout=10)
                        if response.status_code == 200 and link not in ListOfProcessedLinks:
                            ListOfProcessedLinks.append(link)
                            ListOfContents.append(dictOfFeatures)
                        else:
                            ListOfProcessedLinks.append(link)
                            ListOfBadContents.append(dictOfFeatures)
                    except Exception as e:
                        dictOfFeatures[key] = ' '
                        print(f"Error processing link: {link}. Exception: {e}")
    
            except Exception as e:
                    dictOfFeatures[key] = ' '
                    print(f"Error processing link: {link}. Exception: {e}")
                 
        if debug == True:
            if i != 0 and i % 1 == 0:
                print(f"\r{100 * i / len(pastURLs):.2f}%", end='')
                if i == len(pastURLs) - 1:
                    print(f"\r100.00%", end='')

    print(f"Finished processing. Total articles found: {len(ListOfContents)}, Other codes: {len(ListOfTagContents)-len(ListOfContents)-len(ListOfBadContents)}, Bad articles: {len(ListOfBadContents)}")

    path = "data/"
    badfilename = "badnewsPublico2021.json"

    if not os.path.exists(path):
        os.makedirs(path)

    with open(f'{path + filename}', 'w', encoding='utf-8') as fp:
        json.dump(ListOfContents, fp, indent=4, ensure_ascii=False)
    
    with open(f'{path + badfilename}', 'w', encoding='utf-8') as fp:
        json.dump(ListOfBadContents, fp, indent=4, ensure_ascii=False)   

    