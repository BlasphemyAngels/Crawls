#########################################################################
# File Name: taobao_spier.py
# Author: caochenglong
# mail: caochenglong@163.com
# Created Time: 2017-07-23 11:54:32
# Last modified:2017-07-23 11:55:59
#########################################################################
# !/usr/bin/python3
# _*_coding: utf-8_*_

import requests
from selenium import webdriver

driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--load-images=false'])
driver.set_window_size(1400, 900)

#  driver.get('https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.1.1f4d1f26pECRnu&id=553883776914&user_id=2258998827&cat_id=50026329&is_b=1&rn=3bcd79c3c46180f94f07ea4d8d9116c3')

driver.get('https://www.baidu.com')

print(driver.page_source)
driver.close()
