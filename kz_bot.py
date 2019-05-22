# coding=utf-8
from typing import List

from bs4 import BeautifulSoup
import requests
import re

base_url = 'http://kinozal.tv/'
paginator = 'browse.php?page='
page_num = '1'


# url = 'http://kinozal.tv/browse.php?page=1'
url = f'{base_url}{paginator}{page_num}'
proxy = {'http':'167.86.97.101:80'}


def get_html(url):
    req = requests.get(url, proxies=proxy)
    return {'html': req.text, 'status':req.status_code}


def get_soup(html):
    if html['status'] == 200:
        soup: BeautifulSoup = BeautifulSoup(html['html'], 'lxml')
        return soup
    else:
        return None


def get_kz_table(soup):
    table: object = soup.find('table', {'class': 't_peer'})
    return table


def get_today_rows(table):
    search_res = table.findChildren('td', text = re.compile('сегодня'))
    rows: List[object] = []
    for item in search_res:
        assert isinstance(item.parent, object)
        rows.append(item.parent)
    return rows


def main():
    # pass
    html = get_html(url)
    soup = get_soup(html)
    table = get_kz_table(soup)
    rows = get_today_rows(table)
    print(rows)


if __name__ == '__main__':
    main()
