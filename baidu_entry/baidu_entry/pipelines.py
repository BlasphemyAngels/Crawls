# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals


class BaiduEntryPipeline(object):

    def spider_opened(self, spider):
        self._contents = {}

    def process_item(self, item, spider):
        self._contents[item['label']] = item['attr']
        return item

    def spider_closed(self, spider):
        with open("res", "a+") as f:
            for key, value in self._contents.items():
                if key is None:
                    print(key)
                    print(value)
                    continue
                f.write(key + "\t" + str(value) + "\n")

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(
            pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(
            pipeline.spider_closed, signals.spider_closed)
        return pipeline
