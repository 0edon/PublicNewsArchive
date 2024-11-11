import requests
from bs4 import BeautifulSoup
import json
import os
import time

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

    start = time.time()  # Start time for the entire process

    for i in range(len(pastURLs)):
        start2 = time.time()  # Start time for each URL
        try:
            response = requests.get(pastURLs[i], headers=headers, timeout=10, allow_redirects=True)
            if len(response.history) > 5:
                print(f"Redirection chain for URL: {pastURLs[i]}")
                for resp in response.history:
                    print(f"{resp.status_code} -> {resp.url}")
                raise requests.exceptions.TooManyRedirects
            soup = BeautifulSoup(response.content, 'html.parser', from_encoding="UTF-8")
            
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
                    except Exception as e:
                        print(f"Error processing tag: {key}. Exception: {e}")
                        dictOfFeatures[key] = ' '

                try:
                    response = requests.get(link, headers=headers, timeout=10, allow_redirects=True)
                    if len(response.history) > 5:
                        print(f"Redirection chain for link: {link}")
                        for resp in response.history:
                            print(f"{resp.status_code} -> {resp.url}")
                        raise requests.exceptions.TooManyRedirects
                    if response.status_code == 200 and link not in [item['Link'] for item in ListOfContents]:
                        dictOfFeatures[key] = link
                        ListOfContents.append(dictOfFeatures)
                    else:
                        ListOfBadContents.append(link)
                except requests.exceptions.Timeout:
                    print(f"Timeout occurred for link: {link}")
                    ListOfBadContents.append(link)
                except requests.exceptions.TooManyRedirects:
                    print(f"Too many redirects for link: {link}")
                    ListOfBadContents.append(link)
                except Exception as e:
                    print(f"Error processing link: {link}. Exception: {e}")
                    ListOfBadContents.append(link)
        except requests.exceptions.Timeout:
            print(f"Timeout occurred for URL: {pastURLs[i]}")
            ListOfBadContents.append(pastURLs[i])
        except requests.exceptions.TooManyRedirects:
            print(f"Too many redirects for URL: {pastURLs[i]}")
            ListOfBadContents.append(pastURLs[i])
        except Exception as e:
            print(f"Error processing URL: {pastURLs[i]}. Exception: {e}")
            ListOfBadContents.append(pastURLs[i])

        end2 = time.time()  # End time for each URL
        if debug:
            print(f"\r{100 * i / len(pastURLs):.2f}%, Time elapsed for URL: {end2 - start2:.2f} seconds", end='')

    end = time.time()  # End time for the entire process

    print(f"\nFinished processing. Total articles found: {len(ListOfContents)}, Bad articles: {len(ListOfBadContents)}, Total time elapsed: {end - start:.2f} seconds")

    path = "data/"
    bad_articles_filename = "bad_" + filename

    if not os.path.exists(path):
        os.makedirs(path)

    with open(f'{path + filename}', 'w', encoding='utf-8') as fp:
        json.dump(ListOfContents, fp, indent=4, ensure_ascii=False)
    
    with open(f'{path + bad_articles_filename}', 'w', encoding='utf-8') as fp:
        json.dump(ListOfBadContents, fp, indent=4, ensure_ascii=False)