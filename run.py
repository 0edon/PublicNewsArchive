from publicnewsarchive import dataExtraction

pastURLs = dataExtraction.getPastURLs(year='2022', newspaper_url='https://publico.pt/', startMonth='01', endMonth='12')

# dataExtraction.getNewsArticles(pastURLs=pastURLs[:1], news_htmlTag='div',
#                   news_htmlClass='card__inner', links_htmlTag='a', links_htmlClass='card__faux-block-link', filename='newsPublico2021.json', debug=True)