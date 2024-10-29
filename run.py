from publicnewsarchive import dataExtraction

pastURLs = dataExtraction.getPastURLs(year='2021', newspaper_url='https://publico.pt/', startMonth='06', endMonth='07')

print(pastURLs)