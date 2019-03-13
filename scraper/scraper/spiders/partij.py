# -*- coding: utf-8 -*-
import os
import lxml.etree
import lxml.html
import scrapy
import pandas as pd
from scrapy.spiders import BaseSpider
import re


class PartijSpider(scrapy.spiders.Spider):
    if not os.path.isdir('scraper/json'):
        path = 'scraper/json'
        os.mkdir(path)

    name = 'partij'
    with open('scraper/spiders/osf_urls.csv', 'r+') as f:
        data = pd.read_csv(f)
    start_urls = data['Website'][1:].dropna().tolist()
    os.chdir(os.getcwd() + "/json")

    def parse(self, response):
        root = lxml.html.fromstring(response.body)

        # optionally remove tags that are not usually rendered in browsers
        # javascript, HTML/HEAD, comments, add the tag names you dont want at the end
        lxml.etree.strip_elements(root, lxml.etree.Comment, "script", "head")

        # complete text
        page = response.url.split("/")[-2]
        filename = 'partij-%s.json' % page
        data = lxml.html.tostring(root, method="text", encoding='unicode')
        new_data = data.replace('\n', ' ').replace('\r', ' ').replace('"', '').replace('\\', ' ').replace('\t', ' ')
        new_data2 = re.sub(r'\s*(?:https?://)?www\.\S*\.[A-Za-z]{2,5}\s*', ' ', new_data).strip()

        with open(filename, "w") as f:
            f.write("{ \"content\": \"" + new_data2.strip().replace("\n", " ") + "\" }")
