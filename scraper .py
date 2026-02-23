import requests
from bs4 import BeautifulSoup
import json

def scrape_gorla():
    # URL of the news page
    url = "https://comune.gorlaminore.va.it/vivere-gorla-minore/notizie/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        news_list = []
        # Find all article tags (up to 100)
        articles = soup.find_all('article')[:100] 

        for article in articles:
            try:
                # Extract Title
                title = article.find('h3').get_text(strip=True)
                # Extract Link
                link = article.find('a')['href']
                # Extract Date if available
                date = article.find('time').get_text(strip=True) if article.find('time') else ""
                
                # Extract Image URL
                img_tag = article.find('img')
                img_url = img_tag['src'] if img_tag else "https://via.placeholder.com/400x200?text=Gorla+News"
                
                # Fix relative URLs
                if not link.startswith('http'): 
                    link = "https://comune.gorlaminore.va.it" + link
                if not img_url.startswith('http'): 
                    img_url = "https://comune.gorlaminore.va.it" + img_url

                news_list.append({
                    "title": title,
                    "date": date,
                    "img_url": img_url,
                    "url": link
                })
            except:
                continue

        # Save to JSON file with the key "news"
        with open('gorlanews_db.json', 'w', encoding='utf-8') as f:
            json.dump({"news": news_list}, f, ensure_ascii=False, indent=4)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_gorla()
