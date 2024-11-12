import json
import os

path = "data/"
filename = "filtered_processed_articles.json"

def filter_short_articles(input_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            articles = json.load(f)
    except UnicodeDecodeError:
        print(f"Error decoding {input_file}. Please ensure the file is encoded in UTF-8.")
        return
    
    initial_count = len(articles)
    filtered_articles = [article for article in articles if len(article['text'].split()) >= 30]
    filtered_count = len(filtered_articles)
    
    removed_count = initial_count - filtered_count
    print(f'Number of articles removed: {removed_count}')
    
    if not os.path.exists(path):
        os.makedirs(path)

    with open(f'{path + filename}', 'w', encoding='utf-8') as f:
        json.dump(filtered_articles, f, indent=4, ensure_ascii=False)

# Example usage
input_file = 'C:/Users/Tese/Vscode/PublicNewsArchive/data/processed_articles.json'
filter_short_articles(input_file)
