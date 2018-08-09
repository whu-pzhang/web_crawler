#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created by pzhang on 2018/8/9

import requests
from requests.exceptions import RequestException
import re
import json

def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile(
                         '<li>.*?<div class="item">.*?>(\d+)</em>.*?'
                         'href="(.*?)">.*?img.*?src="(.*?)" class.*?'
                         'title">(.*?)</span>.*?'
                         '<br>\\n(.*?)</p>.*?'
                         'class="star">.*?rating_num.*?>(.*?)</span>'
                         , re.S)
    results = re.findall(pattern, html)

    for item in results:
        yield {
            "index": item[0],
            "url": item[1],
            "img_url": item[2],
            "title": item[3],
            "year": item[4].split("&nbsp;")[0].strip(),
            "rate": item[5],
        }

def write_to_file(content):
    with open("result.txt", 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    url = "https://movie.douban.com/top250?start=" + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(10):
        main(i*25)