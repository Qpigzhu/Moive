"""
    爬取PM2.5接口
"""

import requests
from lxml import etree
from requests.exceptions import RequestException


def get_html(url):
    headers = {
        'User - Agent': 'Mozilla / 5.0(Windows NT 6.1;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 55.0.2883.87Safari / 537.36'
    }
    try:
        html = requests.get(url,headers=headers)
        if html.status_code == 200:
            html.encoding = "utf-8"
            return html.text
        return None
    except RequestException:
        return None


def get_info(url):
    aqi_list = []
    html = get_html(url)
    sel = etree.HTML(html)
    aqi = sel.xpath('//div[@class="span1"]/div[1]/text()')[0].strip()
    aqi_list.append(aqi)

    city_name = sel.xpath('//div[@class="city_name"]/h2/text()')[0].strip()
    aqi_list.append(city_name)

    affect = sel.xpath('//div[@class="affect"]/p/text()')[0].strip()
    aqi_list.append(affect)

    action = sel.xpath('//div[@class="action"]/p/text()')[0].strip()
    aqi_list.append(action)

    level = sel.xpath('//div[@class="level"]/h4/text()')[0].strip()
    aqi_list.append(level)
    
    return aqi_list


def main(city):
    url = "http://www.pm25.in/{}".format(city)
    try:
        aqi_list = get_info(url)
    except:
        return None

    return aqi_list




if __name__ == '__main__':
    main("东莞")