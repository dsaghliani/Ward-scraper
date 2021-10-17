from bs4 import BeautifulSoup
import requests
from cloudflare_decryptor import decrypt_cloudflare_email
from pathlib import Path

# It's vital that OUTPUT_DIRECTORY ends with a slash ('/').
OUTPUT_DIRECTORY = 'chapters/'

def scrape_chapter(chapter_url: str):
    response = requests.get(chapter_url)
    soup = BeautifulSoup(response.content, 'lxml', from_encoding = 'utf-8')
    main = soup.find('main')
    article = main.article

    # Fetch the essentials.
    title = article.header.h1
    content = article.find('div', class_='entry-content')

    # Change the root and title tags.
    content.name = 'body'
    del content['class']
    title['class'] = 'chapter-title'

    # Remove the extraneous.
    first_paragraph = content.p
    first_paragraph.decompose()

    for share_item in content.find_all('div', class_='sharedaddy'):
        share_item.decompose()

    # Unwrap all <a> tags and decrypt any email addresses.
    for a_tag in content.find_all('a'):
        if a_tag.has_attr('class') and '__cf_email__' in a_tag['class']:
            fp = a_tag['data-cfemail']
            try:
                a_tag.string = decrypt_cloudflare_email(fp)
            except ValueError:
                pass
        a_tag.unwrap()

    # Insert the title.
    content.insert(0, title)

    # Write the output to a text file.
    Path(OUTPUT_DIRECTORY).mkdir(exist_ok=True)
    with open(f'{OUTPUT_DIRECTORY}{title.text}.txt', 'w', encoding = 'utf-8') as file:
        file.write(content.prettify())
