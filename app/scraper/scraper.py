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

def get_tech_news():
    all_news = []
    all_news.extend(scrape_tecmundo())

    return all_news