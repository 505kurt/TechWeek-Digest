import requests
from bs4 import BeautifulSoup

def scrape_tecmundo():
    url = 'https://www.tecmundo.com.br/'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[TecMundo Error] {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    news_list = []

    for link_tag in soup.select('a:has(h2.styles_title__TRNiL)'):
        title_tag = link_tag.select_one('h2.styles_title__TRNiL')
        if title_tag and link_tag.has_attr('href'):
            title = title_tag.text.strip()
            link = link_tag['href']

            if link.startswith('/'):
                link = 'https://www.tecmundo.com.br' + link
            elif not link.startswith('http'):
                link = 'https://www.tecmundo.com.br/' + link

            news_list.append({
                'title': title,
                'link': link,
                'source': 'TecMundo'
            })

    return news_list

def scrape_techcrunch():
    url = 'https://techcrunch.com/'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[TechCrunch Error] {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    news_list = []

    for link_tag in soup.select('a.loop-card__title-link'):
        title = link_tag.text.strip()
        link = link_tag['href']

        news_list.append({
            'title': title,
            'link': link,
            'source': 'TechCrunch'
        })

    return news_list

def get_tech_news():
    all_news = []
    all_news.extend(scrape_tecmundo())
    all_news.extend(scrape_techcrunch())

    return all_news

def get_article_text(link):
    try:
        response = requests.get(link, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[Article Error] {e}")
        return "Erro ao acessar a notícia."

    soup = BeautifulSoup(response.text, 'html.parser')

    if 'tecmundo.com.br' in link:
        return extract_tecmundo_text(soup)
    elif 'techcrunch.com' in link:
        return extract_techcrunch_text(soup)
    else:
        return "Fonte desconhecida para extração de texto."

    
def extract_tecmundo_text(soup):
    container = soup.select_one('div.styles_main_text__2WIw2')
    
    if not container:
        return "Não foi possível encontrar o corpo da notícia do TecMundo."

    paragraphs = container.select('p.MsoNormal')

    if not paragraphs:
        paragraphs = soup.select('div.styles_main_text__2WIw2 p')
    if not paragraphs:
        paragraphs = soup.select('p')

    text = '\n'.join([p.text.strip() for p in paragraphs if p.text.strip()])

    return text if text else "Não foi possível extrair o texto da notícia do TecMundo."

def extract_techcrunch_text(soup):
    paragraphs = soup.select('p.wp-block-paragraph')
    text = '\n'.join([p.text.strip() for p in paragraphs if p.text.strip()])
    return text if text else "Não foi possível extrair o texto da notícia do TechCrunch."