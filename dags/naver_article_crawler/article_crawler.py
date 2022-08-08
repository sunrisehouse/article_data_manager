import requests
from bs4 import BeautifulSoup

class ArticleCrawler:
    def __init__(self):
        pass

    def crawl(self, url):
        custom_header = {
            'referer': 'https://www.naver.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers = custom_header, verify=False)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            title = soup.select_one('.media_end_head_headline')
            category = soup.select_one('.Nlist_item._LNB_ITEM.is_active')
            date_time = soup.select_one('._ARTICLE_DATE_TIME')
            modify_time = soup.select_one('._ARTICLE_MODIFY_DATE_TIME')
            contents = soup.select_one('#newsct_article')
            writer = soup.select_one('.byline_s')

            title = title.get_text() if title is not None else None
            category = category.get_text() if category is not None else None
            date_time = date_time.get_text() if date_time is not None else None
            modify_time = modify_time.get_text() if modify_time is not None else None
            contents = contents.get_text() if contents is not None else None
            writer = writer.get_text() if writer is not None else None

            return {
                'title': title,
                'category': category,
                'date_time': date_time,
                'modify_time': modify_time,
                'contents': contents,
                'writer': writer,
            }
        else:
            print(response.status_code)
