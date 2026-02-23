import requests
from bs4 import BeautifulSoup
import json

def scarica():
    url = "https://www.comune.gorlaminore.va.it/c012079/po/mostra_news.php"
    base = "https://www.comune.gorlaminore.va.it"
    try:
        r = requests.get(url, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        news = []
        blocchi = soup.select('.elenco-news li') or soup.find_all('div', class_='notizia')
        for b in blocchi:
            t = b.find('h3').text.strip() if b.find('h3') else ""
            if not t: continue
            d = b.find('p').text.strip() if b.find('p') else ""
            dt = b.find('span', class_='data').text.strip() if b.find('span', class_='data') else ""
            l = base + b.find('a')['href'] if b.find('a') else url
            img = base + b.find('img')['src'] if b.find('img') else "https://via.placeholder.com/600x400.png"
            news.append({"title": t, "excerpt": d, "date": dt, "url": l, "img_url": img})
        with open('gorlanews_db.json', 'w', encoding='utf-8') as f:
            json.dump({"news": news[:100]}, f, ensure_ascii=False, indent=4)
        print("Fatto!")
    except Exception as e: print(f"Errore: {e}")

if __name__ == "__main__": scarica()
