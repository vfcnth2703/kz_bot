# coding=utf-8
import re
from typing import List

import requests
from bs4 import BeautifulSoup

base_url = 'http://kinozal.tv/'
paginator = 'browse.php?page='
page_num = '1'

# url = 'http://kinozal.tv/browse.php?page=1'
url = f'{base_url}{paginator}{page_num}'
proxy = {'http': '167.86.97.101:80'}


def get_html(url):
    req = requests.get(url, proxies=proxy)
    return {'html': req.text, 'status': req.status_code}


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
    search_res = table.findChildren('td', text=re.compile('сегодня'))
    rows: List[object] = []
    for item in search_res:
        assert isinstance(item.parent, object)
        rows.append(item.parent)
    return rows


class KzParser:
    def __init__(self):
        self.category = ''
        self.name = ''
        self.year = ''
        self.commentary_cnt = 0
        self.size = ''
        self.seeds = 0
        self.peers = 0
        self.uploaded = ''
        self.super_seed = {'href': '',
                           'nick': ''}

    def set_data_fields(self, data):
        try:
            self.category = int(
                data.find('img', {'class': 'pointer'}).attrs['onclick'].replace('(', ' ').replace(')', ' ').split()[1])
        except:
            self.category = ''
        try:
            self.name = data.find('td', {'class': 'nam'}).text.split('/')[0]
        except:
            self.name = ''
        try:
            self.year = data.find('td', {'class': 'nam'}).text.split('/')[2]
        except:
            self.year = ''
        try:
            self.commentary_cnt = data.find_all('td', {'class': 's'})[0].text
        except:
            self.commentary_cnt = 0
        try:
            self.size = data.find_all('td', {'class': 's'})[1].text
        except:
            self.size = ''
        try:
            self.uploaded = data.find_all('td', {'class': 's'})[2].text
        except:
            self.uploaded = ''
        try:
            self.seeds = data.find('td', {'class': 'sl_s'}).text
        except:
            self.seeds = 0
        try:
            self.peers = data.find('td', {'class': 'sl_p'}).text
        except:
            self.peers = 0
        try:
            self.super_seed['href'] = data.find('a', {'class': 'u5'}).attrs['href']
        except:
            self.super_seed['href'] = ''
        try:
            self.super_seed['nick'] = data.find('a', {'class': 'u5'}).get_text()
        except:
            self.super_seed['nick'] = ''
        return self


def main():
    kz = KzParser()
    html = get_html(url)
    soup = get_soup(html)
    table = get_kz_table(soup)
    rows = get_today_rows(table)
    for row in rows:
        row_data: KzParser = kz.set_data_fields(row)
        print(row_data.name, row_data.year)


if __name__ == '__main__':
    main()
