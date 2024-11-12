from newspaper import Article
import newspaper.configuration
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from newspaper.article import ArticleException
import os

config = newspaper.configuration.Configuration()
config.request_timeout = 30
config.language = 'pt'

# Step 1: Read the JSON file
with open('C:/Users/Tese/Vscode/PublicNewsArchive/data/saponews2022.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Step 2: Extract the links
links = [item['Link'] for item in data]

start2 = time.time()

# Process only the first 1000 links
# links = links[:10]

articles_data = []
source_url = 'https://www.sapo.pt/'

def process_article(link, retries=3):
    for attempt in range(retries):
        try:
            start = time.time()
            article = Article(link, config=config)  # Initialize with the URL and config
            article.download()       # Download the article content
            article.parse()          # Parse the downloaded content

            article_data = {
                "source_url": source_url ,
                "title": article.title,
                "text": article.text,
                "publish_date": article.publish_date.isoformat() if article.publish_date else None,
            }
            end = time.time()
            print(f"Article processed in {end - start:.2f} seconds.")
            return article_data
        except ArticleException as e:
            print(f"Attempt {attempt + 1} failed for URL {link}: {e}")
            time.sleep(2)  # Wait before retrying
    return None

# Step 3: Process the articles with multithreading
max_workers = 40  # Adjust the number of threads as needed

with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = {executor.submit(process_article, link): link for link in links}
    for future in as_completed(futures):
        link = futures[future]
        try:
            article_data = future.result()
            if article_data:
                articles_data.append(article_data)
                print(f"Processed {len(articles_data)} articles.")
        except Exception as e:
            print(f"Failed to process article: {e}")

# Save the processed articles to a JSON file
path = "data/"
filename = "processed_articles.json"

if not os.path.exists(path):
    os.makedirs(path)

with open(f'{path + filename}', 'w', encoding='utf-8') as fp:
    json.dump(articles_data, fp, indent=4, ensure_ascii=False)

end2 = time.time()
print(f"Processed articles saved to 'processed_articles.json', Total time elapsed: {end2 - start2:.2f} seconds.")
