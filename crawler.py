from bs4 import BeautifulSoup
from selenium import webdriver
import re
import datetime

def yahoo_sport_crawler(driver):
    url = 'https://news.yahoo.co.jp/categories/sports'
    driver.get(url)
    data = driver.page_source
    soup = BeautifulSoup(data, 'html.parser')
    all_items = soup.find_all(name = 'a', attrs = 'newsFeed_item_link')
    result = []
    for item in all_items:
        item_dict = dict()
        item_dict['img_link'] = item.find(name = 'img').get('src')
        item_dict['news_link'] = item.get('href')
        item_dict['title'] = item.find(name = 'div', attrs = ['newsFeed_item_title']).text
        pub_date = item.find(name = 'time', attrs = ['newsFeed_item_date']).text
        strinfo = re.compile(r'[(](.*?)[)]')
        pub_date = strinfo.sub('', pub_date)
        pub_date = str(datetime.datetime.now().year) + '/' + pub_date
        item_dict['pub_time'] = pub_date
        item_dict['website'] = 'yahoo'
        result.append(item_dict)
    return result

def nhk_sport_crawler(driver):
    url = 'https://www3.nhk.or.jp/news/cat07.html?utm_int=all_header_menu_news-sports'
    driver.get(url)
    data = driver.page_source
    soup = BeautifulSoup(data, 'html.parser')
    all_items = soup.find(name = 'ul', attrs = 'content--list grid--col-single')
    all_items = all_items.find_all(name = 'dl')
    result = []
    for item in all_items:
        item_dict = dict()
        item_dict['news_link'] = 'https://www3.nhk.or.jp' + item.find(name = 'a').get('href').split('?')[0]
        item_dict['img_link'] = 'https://www3.nhk.or.jp' + item.find(name = 'img').get('src')
        item_dict['title'] = item.find(name = 'em', attrs = ['title']).text
        item_dict['pub_time'] = item.find(name = 'time').get('datetime').replace('T', ' ').replace('-', '/')
        item_dict['website'] = 'nhk'
        result.append(item_dict)
    return result

def crawler_all():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome('put the driver here!!!!!!!!', chrome_options=chrome_options)
    yh_result = yahoo_sport_crawler(driver)
    nhk_result = nhk_sport_crawler(driver)
    all = yh_result + nhk_result
    all.sort(key = lambda date: datetime.datetime.strptime(date['pub_time'], "%Y/%m/%d %H:%M"))
    driver.close()
    return all