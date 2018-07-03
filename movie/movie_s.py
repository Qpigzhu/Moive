"""
    爬取电影网页
"""
import requests
from lxml import etree
from requests.exceptions import RequestException

import os,django
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie.settings")
django.setup()

from movieapp.models import Movie

def get_html(url):
    headers = {
      'user-agent':'Mozilla / 5.0(WindowsNT6.1;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 66.0.3359.139Safari / 537.36'
    }
    try:
        html = requests.get(url,headers = headers)
        if html.status_code == 200:
            html.encoding = 'gb2312'
            return html.text
        return None
    except RequestException:
        return None

def get_info(url):
    html = get_html(url)
    sel = etree.HTML(html)
    infos = sel.xpath('//table[@class="tbspan"]')
    for info in infos:
        name = info.xpath('tr[2]/td[2]/b/a/text()')[0]
        url = info.xpath('tr[2]/td[2]/b/a/@href')[0]
        yield {
            'name' : name,
            'url':url,
        }


def get_movie_datil(movie_html):
    html = get_html(movie_html)
    sel = etree.HTML(html)
    jpg = sel.xpath('//img[@border="0"]/@src')[1]
    url = sel.xpath('//td[@style="WORD-WRAP: break-word"]/a/@href')[0]
    return jpg,url

#判断电影是否存在数据库，存在返回False，不存在返回Ture
def _is_included(title):
        try:
            m = Movie.objects.get(title=title)
            return False
        except:
            return True


    
def pa():
    for j in range(1,20):
        if j != 1:
            url = 'http://www.dytt8.net/html/gndy/dyzz/list_23_{}.html'.format(j)
        else:
            url = 'http://www.dytt8.net/html/gndy/dyzz/index.html'
        for i in get_info(url):
            urls = i.get('url')
            title = i.get('name')
            urls = 'http://www.dytt8.net{}'.format(str(urls))
            jpg,url = get_movie_datil(urls)

            # 判断电影是否存在数据库，存在返回False，不存在返回Ture
            if _is_included(title):
                movie_models = Movie.objects.create(title=title,jpg=jpg,download=url)
                movie_models.save()



if __name__ == '__main__':
    pa()

