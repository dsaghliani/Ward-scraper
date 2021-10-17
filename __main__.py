import toc_scraper
import chapter_scraper

if __name__ == '__main__':
    urls = toc_scraper.scrape_toc_links()
    for url in urls:
        chapter_scraper.scrape_chapter(url)