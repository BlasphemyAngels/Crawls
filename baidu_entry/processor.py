#########################################################################
# File Name: test.py
# Author: caochenglong
# mail: caochenglong@163.com
# Created Time: 2017-07-21 13:06:47
# Last modified:2017-07-21 13:07:05
#########################################################################
# !/usr/bin/python3
# _*_coding: utf-8_*_

import rdflib
import bs4

pattern_c = ""

class BaiduEntryItem(object):
    url = None
    text = None


class BaiduEntry_Processor(object):

    def process(self, filepath):
        with open(filepath, "r") as f:
            lines = f.readlines()
            for line in lines:
                infos = line.split('\t')
                attr = eval(infos[1])
                for key, value in attr.items():
                    if "<dd" in value:
                        soup = bs4.BeautifulSoup(value, "html.parser")
                        print(soup.text)

    def dump_dict(self):
        pass


def main():
    processor = BaiduEntry_Processor()
    processor.process("res")


if __name__ == "__main__":
    main()
