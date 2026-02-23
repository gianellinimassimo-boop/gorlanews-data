import requests
from bs4 import BeautifulSoup
import json

def scarica_notizie():
    url_comune = "https://www.comune.gorlaminore.va.it/c012079/po/mostra_news.php"
    base_url = "https://www.comune.gorlaminore.va.it"
    try:
        risposta = requests.get(url_comune, timeout=15)
        risposta.raise_for_status()
        zuppa = BeautifulSoup(risposta.text, 'html.parser')
        nuova_lista_news = []
        blocchi = zuppa.select('.elenco-news li') or zuppa.find_all('div', class_='notizia')
        for blocco in blocchi:
            try:
                titolo = blocco.find('h3').text.strip() if blocco.find('h3') else ""
                if not titolo: continue
                descrizione = blocco.find('p').text.strip() if blocco.find('p') else ""
                data = blocco.find('span', class_='data').text.strip() if blocco.find('span', class_='data') else ""
                link_tag = blocco.find('a', href=True)
                link_completo = base_url + link_tag['href'] if link_tag else url_comune
                img_tag = blocco.find('img', src=True)
                img_url = base_url + img_tag['src'] if img_tag else "https://via.placeholder.com/600x400.png?text=Gorla+News"
                nuova_lista_news.append({"title": titolo, "excerpt": descrizione, "date": data, "url": link_completo, "img_url": img_url})
            except: continue
        with open('gorlanews_db.json', 'w', encoding='utf-8') as f:
            json.dump({"news": nuova_lista_news[:100]}, f, ensure_ascii=False, indent=4)
        print("Database aggiornato!")
    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    scarica_notizie()
