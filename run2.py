from newspaper import Article
import json

# Step 1: Read the JSON file
with open('C:/Users/Tese/Vscode/PublicNewsArchive/data/news2022.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Step 2: Extract the links
links = [item['Link'] for item in data]

articles_data = []

proxies = {
    'http': 'http://8.211.42.167:3128',
    'https': 'https://3.127.62.252:80'
}

for link in links:
    article = Article(link, proxies=proxies)  # Initialize with the URL
    article.download()       # Download the article content
    article.parse()          # Parse the downloaded content

    article_data = {
        "url": link,
        "title": article.title,
        "text": article.text,
        "authors": article.authors,
        "publish_date": article.publish_date.isoformat() if article.publish_date else None,
    }

    articles_data.append(article_data)

path = "data/"
filename = "processed_articles.json"

with open(f'{path + filename}', 'w', encoding='utf-8') as fp:
    json.dump(articles_data, fp, indent=4, ensure_ascii=False)

print("Processed articles saved to 'processed_articles.json'")