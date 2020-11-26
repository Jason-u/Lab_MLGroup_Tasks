#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
from bs4 import BeautifulSoup
import csv


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'}
url = 'http://lishi.tianqi.com/xian/'
dates = [str(i) for i in range(201101, 201113)] + [str(i) for i in range(201201, 201213)]\
        + [str(i) for i in range(201301, 201313)] + [str(i) for i in range(201401, 201413)]\
        + [str(i) for i in range(201501, 201513)] + [str(i) for i in range(201601, 201613)]\
        + [str(i) for i in range(201701, 201713)] + [str(i) for i in range(201801, 201813)]\
        + [str(i) for i in range(201901, 201913)] + [str(i) for i in range(202001, 202011)]

with open('./WeatherData.csv', 'w', newline='') as out_file:
    filewriter = csv.writer(out_file)
    filewriter.writerow(['日期', '星期', '最高气温', '最低气温', '天气', '风向', '风力'])
    for date in dates:
        new_url = url + date + '.html'
        print('正在爬取并写入' + date + '的数据...')
        response = requests.get(url=new_url, headers=headers)
        page_text = response.text
        soup = BeautifulSoup(page_text, 'html.parser')
        ul = soup.find('ul', class_='thrui')
        li_list = ul.find_all('li')
        for i in range(len(li_list)):
            info_txt = li_list[i].text.lstrip().rstrip()
            info_list = info_txt.split()
            filewriter.writerow(info_list)
        print(date + '的数据写入成功！')
    print('写入工作已完成！')
