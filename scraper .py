import requests
from bs4 import BeautifulSoup
import json

def scrape_gorla():
    url = "https://comune.gorlaminore.va.it/vivere-gorla-minore/notizie/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    news_list = []
    # Prende gli articoli dal sito
    articles = soup.find_all('article')[:100] 

    for article in articles:
        try:
            title = article.find('h3').get_text(strip=True)
            link = article.find('a')['href']
            date = article.find('time').get_text(strip=True) if article.find('time') else ""
            img_tag = article.find('img')
            img_url = img_tag['src'] if img_tag else "https://via.placeholder.com/400x200?text=Gorla+News"
            
            if not link.startswith('http'): link = "https://comune.gorlaminore.va.it" + link
            if not img_url.startswith('http'): img_url = "https://comune.gorlaminore.va.it" + img_url

            news_list.append({
                "title": title,
                "date": date,
                "img_url": img_url,
                "url": link
            })
        except:
            continue

    # SALVA CON LA CHIAVE "news" (fondamentale per l'app!)
    with open('gorlanews_db.json', 'w', encoding='utf-8') as f:
        json.dump({"news": news_list}, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    scrape_gorla()
