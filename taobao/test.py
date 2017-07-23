#########################################################################
# File Name: test.py
# Author: caochenglong
# mail: caochenglong@163.com
# Created Time: 2017-07-23 12:08:30
# Last modified:2017-07-23 12:10:46
#########################################################################
# !/usr/bin/python3
# _*_coding: utf-8_*_
#使用selenium+Carome/phantomJS模拟浏览器爬取淘宝商品信息
# 思路：
# 第一步：利用selenium驱动浏览器，搜索商品信息，得到商品列表
# 第二步：分析商品页数，驱动浏览器翻页，并得到商品信息
# 第三步：爬取商品信息
# 第四步：存储到mongodb
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 声明浏览器对象，这里定为Chrome
# browser = webdriver.Chrome()
# 声明浏览器对象，可以使用PhanttomJS,这是无界面浏览器，可以设置不加载图片，启用缓存等加快速度
browser = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--load-images=false'])
KEYWORDS="美食"
browser.set_window_size(1400, 900)  # 默认的窗口比较小，为避免影响操作需设定

# 传入搜索关键词并搜索
# 在这里，需要等待搜索框与搜索按钮加载出来完毕，方可传入关键词，并点击搜索
wait = WebDriverWait(browser, 10)  # 表示给browser浏览器一个10秒的加载时间

def search():
    print('正在搜索……')
    try:
        # 驱动浏览器打开网页
        browser.get('https://www.taobao.com/')
        input = wait.until(EC.presence_of_element_located((By.ID, 'q')))  # 表示在规定时间内等待，直到id为q的元素加载出来,注意传入的是元组
        input.send_keys(KEYWORDS)
        # 同样的道理，搜索的按钮也需要等待，直到按钮加载出来,是可以点击的
        button = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))  # 表示规定时间内，搜索按钮是否是可点击的
        button.click()
        #页面加载完成后，找到总页数
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total')))

        get_product()
        return total.text
    except TimeoutException:
        return search()

    # # 得到当前页面的html
    # html = browser.page_source

def next_page(page_number):
    print('正在翻页……')
    try:
        #等待页码框加载完成
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > input')))

        #等待确定按钮可点击，然后点击
        button  = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))

        # 清空并输入页码
        input.clear()
        input.send_keys(page_number)

        button.click()

        #检查当前页是否切换 text_to_be_present_in_element 某个元素文本包含某文字
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_number)))

        get_product()
    except TimeoutException:
        next_page(page_number)


def get_product():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist > div')))
    html = browser.page_source
    doc = pq(html)
    lis = doc('#mainsrp-itemlist .items .item').items()
    for item in lis:
        product={
            'title':item.find('.title').text(),#find方法是为了嵌套找出来，防止遗漏
            'price':item.find('.price').text(),
            'deal':item.find('.deal-cnt').text(),
            'shop':item.find('.shop').text(),
            'location':item.find('.location').text(),
            'image':item.find('.pic .img').attr('src')
        }
        print(product)


def main():

    try:
        total = search()
        total = int(re.compile(r'(\d+)').search(total).group(1))#正则提取页数
        for page_number in range(2,total + 1):
            next_page(page_number)

    except Exception:
        print('出错了')

    finally:
        browser.close()

if __name__=='__main__':
    main()

