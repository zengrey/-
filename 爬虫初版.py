# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 15:10:19 2022

@author: reyze
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import requests
import csv


# 定义论文类
class Paper:
    def __init__(self, title,date):
        self.title = title
        self.date=date


# 进入知网首页并搜索关键词
def driver_open(driver, key_word):
    url = "https://www.cnki.net/"
    driver.get(url)
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR,'#txt_SearchText').send_keys(key_word)
    time.sleep(2)
    # 点击搜索按钮
    driver.find_element(By.CSS_SELECTOR,'body > div.wrapper.section1 > div.searchmain > div > div.input-box > input.search-btn').click()
    time.sleep(5)
    content = driver.page_source.encode('utf-8')
    # driver.close()
    soup = BeautifulSoup(content, 'lxml')
    return soup

def spider(driver, soup, papers):
    tbody = soup.find_all('tbody')
    tbody = BeautifulSoup(str(tbody[0]), 'lxml')
    tr = tbody.find_all('tr')

    for item in tr:
        tr_bf = BeautifulSoup(str(item), 'lxml')

        td_name = tr_bf.find_all('td', class_ = 'name')
        td_name_bf = BeautifulSoup(str(td_name[0]), 'lxml')
        a_name = td_name_bf.find_all('a')
 
        title = a_name[0].get_text().strip()

        td_date = tr_bf.find_all('td', class_ = 'date')
        td_date_bf = BeautifulSoup(str(td_date[0]), 'lxml')
        a_date = td_date_bf.find_all('td')
        date = a_date[0].get_text().strip()

        paper = Paper(title,date)
        papers.append(paper)
        time.sleep(1)   # 每调一次spider休息1s


# pn表示当前要爬的页数
def change_page(driver, pn):
    driver.find_element(By.CSS_SELECTOR,'#page' + str(pn)).click()
    time.sleep(5)
    content = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(content, 'lxml')
    return soup
def change(pn):
    driver.find_element(By.CSS_SELECTOR,'#page' + str(pn)).click()
    time.sleep(10)
    
if __name__ == '__main__':
    driver = webdriver.Chrome("D:\google\chromedriver.exe")
    soup = driver_open(driver, '新型冠状肺炎')  
    papers = []     # 用于保存爬取到的论文
    # 将爬取到的论文数据放入papers中
    for cn in range(9,60,3):
        change(cn)
    for pn in range(60,80):
        content = change_page(driver, pn)
        if len(content.find_all('tbody'))==0:
            print('dd')
            time.sleep(20)
            content = driver.page_source.encode('utf-8')
            soup = BeautifulSoup(content, 'lxml')
            spider(driver, soup, papers)
        elif len(content.find_all('tbody'))!=0:
         spider(driver, content, papers)
         print(pn)
    driver.close()


    # 写入文件
    f_papers_authors = open('./paper_author.csv', 'w', encoding = 'utf-8-sig', newline = '')
    writer_p_a = csv.writer(f_papers_authors)  
    writer_p_a.writerow(["title","date"])    
    
    # 读取每一篇论文
    for paper in papers:
                writer_p_a.writerow([paper.title,paper.date])

    # 关闭文件
    f_papers_authors.close()
