from publicnewsarchive import dataExtraction

pastURLs = dataExtraction.getPastURLs(year='2022', newspaper_url='https://publico.pt/', startMonth='01', endMonth='2')

dataExtraction.getNewsArticles(pastURLs=pastURLs[:2], news_htmlTag='div',
                   news_htmlClass='article__inner', links_htmlTag='a', links_htmlClass='', filename='newsPublico2022.json', debug=True)
