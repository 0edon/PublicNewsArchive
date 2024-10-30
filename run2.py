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
    
    dictOfTags = {'Link': [links_htmlTag, links_htmlClass],}

    ListOfContents = []
    ListOfProcessedLinks = []


    for i in range(len(pastURLs)):
        page = requests.get(pastURLs[i])
        soup = BeautifulSoup(page.content, 'html.parser', from_encoding="UTF-8")
        ListOfTagContents = soup.find_all(news_htmlTag, class_=news_htmlClass)
        for content in ListOfTagContents:
            dictOfFeatures = {}
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
                            print("selinium goes here or maybe add the ones that wont work to a list and then go to the wayback machine isntead of selinium")     
                    except:
                        dictOfFeatures[key] = ' '
            except:
                dictOfFeatures[key] = ' '    

                    

            if link not in ListOfProcessedLinks:
                ListOfProcessedLinks.append(link)
                ListOfContents.append(dictOfFeatures)

        if debug == True:
            if i != 0 and i % 1 == 0:
                print(f"\r{100 * i / len(pastURLs):.2f}%", end='')
                if i == len(pastURLs) - 1:
                    print(f"\r100.00%", end='')
    path = "data/"

    if not os.path.exists(path):
        os.makedirs(path)

    with open(f'{path + filename}', 'w', encoding='utf-8') as fp:
        json.dump(ListOfContents, fp, indent=4, ensure_ascii=False)

getNewsArticles(pastURLs="https://arquivo.pt/noFrame/replay/20210626061200/https://www.publico.pt/", news_htmlTag='div',
                 news_htmlClass='card__inner', links_htmlTag='a', links_htmlClass='card__faux-block-link', filename='newsPublico2021.json', debug=True)