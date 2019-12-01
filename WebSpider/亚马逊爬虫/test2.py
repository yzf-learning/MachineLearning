# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 22:26:21 2019

@author: Admin
"""


from lxml import etree



def getxpath(html):           #返回html的xml结构
    return etree.HTML(html)

sample="""<html>
  <head>
    <title>My page</title>
  </head>
  <body>
    <h2>Welcome to my <a href="#" src="x">page</a></h2>
    <p>This is the first paragraph.</p>
    <!-- this is the end -->
  </body>
</html>
"""



s1=getxpath(sample)
s1.xpath('//title/text()')          #根据绝对路径取出内容



import requests
from bs4 import BeautifulSoup
#https://www.amazon.com/s?k=andalou&__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&ref=nb_sb_noss

url = 'https://www.amazon.com/s?k=andalou&__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&ref=nb_sb_noss'

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/69.0.3486.0 Safari/537.36'}

response = requests.get(url=url, headers=header)
response.encoding = 'utf-8'

f = open("data.txt","r",encoding='utf-8')   #设置文件对象
str_data = f.read()     #将txt文件的所有内容读入到字符串str中


print(response.text)

soup = BeautifulSoup(response.text, 'lxml')
#print(soup)

weather = soup.find('ul', class_='t clearfix')
# 直接输出定位候的元素
#print(weather)

s2=getxpath(response.text)
#s2=getxpath(str_data)


print(s2.xpath('//div[@class="a-section a-spacing-none"]/@href'))

