# -*- coding: utf-8 -*-
import os
import scrapy
import re

from baidu_entry.items import BaiduEntryItem


class BaiduSpiderSpider(scrapy.Spider):
    name = 'baidu_spider'
    start_urls = []
    url_type_dict = {}
    url_class_dict = {}

    url_pattren = r"(.*?)(((ht|f)tps?):\/\/[\w\-]+(\.[\w\-]+)" +\
        "+([\w\-\.,@?^=%&:\/~\+#]*[\w\-\@?^=%&\/~\+#])?)"

    def __init__(self):
        super().__init__(self)
        self.start_urls = self._get_urls()

    def _get_urls(self):
        """ get all of the urls from data dir needed to crawl """
        url_list = []
        filename = "./urls/"
        files = os.listdir(filename)
        pattern = re.compile(self.url_pattren)
        for url_file in files:
            urls_file = os.listdir("urls/" + url_file)
            for urls in urls_file:
                with open("urls/" + url_file + "/" + urls, "r") as f:
                    lines = f.readlines()
                    for line in lines:
                        match = pattern.match(line)
                        if match:
                            ans_url = match.group(2)
                            url_list.append(ans_url)
                            self.url_class_dict[ans_url] = urls[:urls.rfind(
                                '.')]
                            self.url_type_dict[ans_url] = url_file
        #  return url_list[0:30]
        return ['https://baike.baidu.com/item/%E6%9D%8E%E7%99%BD/1043?fr=aladdin']

    def parse(self, response):
        box = response.css(
            'body > div.body-wrapper > div.content-wrapper > \
            div > div.main-content > div.basic-info.cmn-clearfix')
        dls = box.xpath("dl")
        entryItem = BaiduEntryItem()
        entryItem['label'] = response.css("dd > h1::text").extract_first()
        attr = dict()
        for dl in dls:
            d_nums = len(dl.xpath('dt'))
            for i in range(d_nums):
                dt = dl.xpath('dt[%s]/text()' % (i + 1)).extract_first()
                dd = dl.xpath('dd[%s]' % (i + 1)).extract_first()
                attr[dt] = dd
        attr['url'] = response.url
        entryItem['attr'] = attr
        yield entryItem
