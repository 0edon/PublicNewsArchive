from publicnewsarchive import dataExtraction

pastURLs = dataExtraction.getPastURLs(year='2022', newspaper_url='https://sapo.pt', startMonth='11', endMonth='12')

dataExtraction.getNewsArticles(pastURLs=pastURLs, news_htmlTag='article',
                   news_htmlClass='article', links_htmlTag='a', links_htmlClass='', filename='news2022.json', debug=True)

