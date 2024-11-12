from publicnewsarchive import dataExtraction
import json

# pastURLs = dataExtraction.getPastURLs(year='2022', newspaper_url='https://sapo.pt', startMonth='01', endMonth='12')

with open('data/past_urls_2022.json', 'r', encoding='utf-8') as file:
    pastURLs = json.load(file)

dataExtraction.getNewsArticles(pastURLs=pastURLs, news_htmlTag='article',
                   news_htmlClass='article', links_htmlTag='a', links_htmlClass='', filename='saponews2022.json', debug=True)

