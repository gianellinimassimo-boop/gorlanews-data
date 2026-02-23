import requests
from bs4 import BeautifulSoup
import json

def scarica_notizie():
    url = "https://www.comune.gorlaminore.va.it/it/news"
    base_url = "https://www.comune.gorlaminore.va.it"
    
    try:
        r = requests.get(url, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        notizie_estratte = []
        
        # Cerchiamo i blocchi delle notizie (il selettore 'div.v-card' è comune in molti siti comunali italiani)
        articoli = soup.find_all('div', class_='v-card') or soup.select('.elenco-news li')

        for art in articoli:
            # 1. Estrazione Titolo
            titolo = art.find('h3').get_text(strip=True) if art.find('h3') else ""
            if not titolo: continue

            # 2. Estrazione Data Originale dal Sito
            # Cerchiamo tag come <time> o span con classe 'date'
            data_tag = art.find('span', class_='date') or art.find('time')
            data_sito = data_tag.get_text(strip=True) if data_tag else "Data non disponibile"

            # 3. Estrazione Immagine
            img_tag = art.find('img')
            if img_tag and img_tag.get('src'):
                img_url = img_tag['src']
                if not img_url.startswith('http'):
                    img_url = base_url + img_url
            else:
                # Immagine di default se la notizia non ha foto
                img_url = "https://via.placeholder.com/600x400.png?text=Comune+di+Gorla+Minore"

            # 4. Link alla notizia completa
            link_tag = art.find('a')
            link_completo = base_url + link_tag['href'] if link_tag and link_tag['href'].startswith('/') else link_tag['href'] if link_tag else url

            notizie_estratte.append({
                "title": titolo,
                "date": data_sito,
                "img_url": img_url,
                "url": link_completo
            })

        # Salviamo tutto nel file JSON che leggerà Android Studio
        with open('gorlanews_db.json', 'w', encoding='utf-8') as f:
            json.dump({"news": notizie_estratte[:20]}, f, ensure_ascii=False, indent=4)
        
        print(f"Successo! Trovate {len(notizie_estratte)} notizie.")

    except Exception as e:
        print(f"Errore durante lo scraping: {e}")

if __name__ == "__main__":
    scarica_notizie()
