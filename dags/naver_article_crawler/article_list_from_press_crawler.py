import requests
from bs4 import BeautifulSoup
from time import sleep

class ArticleListFromPressCrawler:
    def __init__(self):
        pass

    def crawl(self, oid, date_string):
        custom_header = {
            'referer': 'https://www.naver.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }
        url = f'https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid={oid}&listType=title&date={date_string}'
        response = requests.get(url, headers = custom_header, verify=False)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            page_total_count = len(list(filter(lambda x: x != '\n', list(soup.select_one('.paging').children))))

            a_list = []
            for page_num in range(1, page_total_count + 1):
                page_url = url + f'&page={page_num}'
                page_response = requests.get(page_url, headers = custom_header, verify=False)
                if page_response.status_code == 200:
                    html = response.text
                    soup = BeautifulSoup(html, 'html.parser')
                    news_list = soup.select_one('.list_body.newsflash_body')
                    ali = news_list.select('a')
                    ali = list(map(lambda a: { 'href': a.attrs.get('href') or '', 'title': a.get_text() }, ali))
                    ali = list(filter(lambda a: a.get('href').find('https://n.news.naver.com/mnews/article/') != -1, ali))
                    a_list.extend(ali)
        
                else:
                    print('error with url: ', page_url)
                
                sleep(1)
            return a_list


        else:
            print(response.status_code)
