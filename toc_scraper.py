from bs4 import BeautifulSoup
import requests

DOMAIN = 'https://www.parahumans.net'

def scrape_toc_links():
    response = requests.get(f'{DOMAIN}/table-of-contents')
    soup = BeautifulSoup(response.content, 'lxml', from_encoding = 'utf-8')

    toc = soup.find('div', class_='entry-content')

    # Remove the first two paragraphs.
    for i in range(2):
        toc.p.decompose()

    # Get the <a> tags and retrieve the URLs within.
    a_tags = toc.find_all('a')
    url_retriever = lambda a: f"{DOMAIN}{a['href']}"
    urls = map(url_retriever, a_tags)

    return list(urls)
