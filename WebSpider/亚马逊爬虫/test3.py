# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 17:50:10 2019

@author: Admin
"""

# 美国amazon
import requests,urllib
import datetime
from urllib.parse import quote,unquote
from selenium_operate import ChromeOperate
import re
import time
from crawl_tool_for_py3 import crawlerTool as ct
import os,base64
import xlsxwriter
from PIL import Image

def img_resize(infile,outfile):
    im = Image.open(infile)
    # (x, y) = im.size  # read image size
    x_s = 120  # define standard width
    y_s = 160  # calc height based on standard width
    out = im.resize((x_s, y_s), Image.ANTIALIAS)  # resize image with high-quality
    out.save(outfile)


def gen_xls(item_infos):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    book = xlsxwriter.Workbook('amazon%s.xlsx'%timestamp)
    worksheet = book.add_worksheet('demo')
    worksheet.write_row(0,0, ['关键词','排名','宝贝图片','价格','宝贝类目','宝贝描述','宝贝链接','宝贝评论','宝贝好评'])
    worksheet.set_column('A:D', 15) # 列宽约等于8像素 行高约等于1.37像素
    worksheet.set_column('C:C', 20)
    worksheet.set_column('B:B', 10)
    worksheet.set_column('F:F', 50)
    for i in range(len(item_infos)):
        col = i+1
        try:
            item_info = item_infos[i]
            row =   [item_info['keyword'],item_info['rank'],'',item_info['price'],item_info['cat'],item_info['descriptions'],item_info['item_url'],item_info['comments'],item_info['histograms']]
            worksheet.write_row(col,0, row)
            worksheet.set_row(col, 120)
            if 'item_pic_base64' in item_info:
                item_pic_base64 = item_info["item_pic_base64"]
                try:
                    if 'https:' in item_pic_base64:
                        data = ct.get(item_pic_base64)
                    else:
                        data = base64.b64decode(item_pic_base64)
                    with open('test.png', 'wb') as f:
                        f.write(data)
                    img_resize('test.png', 'img/tmp%s.png'%i)
                    worksheet.insert_image( col,2, 'img/tmp%s.png'%i) # 名字必须不同
                except Exception as e:
                    print(str(e))
        except Exception as e:
            print(e,item_info)
    print('完成结果数,%s'%col)
    book.close()




def extractor_page(page): # 解析宝贝页
    item_info = {"descriptions":""}
    descriptions = ct.getXpath('//div[@id="productDescription"]/p/text()',page)
    if not descriptions:
        descriptions = ct.getXpath( '//div[@id="aplus"]/div//p//text()', page)
    descriptions= ''.join([description.strip() for description in descriptions])
    item_info["descriptions"] = descriptions
    item_pic_base64 = ct.getXpath1( '//div[@id="imgTagWrapperId"]/img/@src', page).split('base64,')[-1]
    item_info["item_pic_base64"] = item_pic_base64
    price = ct.getXpath1( '//span[@id="priceblock_ourprice"]/text()', page)
    item_info["price"] = price
    cats =  ct.getXpath( '//div[@id="wayfinding-breadcrumbs_container"]//a/text()', page)
    item_info["cat"] = '/'.join([cat.strip() for cat in cats])
    
    comments =  ct.getXpath( '//div[@id="reviewsMedley"]//h2/text()', page)
    item_info["comments"] = '/'.join([comment.strip() for comment in comments])
    
    histograms =  ct.getXpath( '//table[@id="histogramTable"]//span[@class="a-size-base"]/text()', page)
    item_info["histograms"] = '/'.join([histogram.strip() for histogram in histograms])
    
    for k,v in item_info.items():
        print (k,v)
    return item_info


item_infos = []

item_url='https://www.amazon.com/dp/B07WG9RPTR/ref=sr_1_1_sspa?keywords=andalou&qid=1571461811&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExR1NRTE05NUo2V0M4JmVuY3J5cHRlZElkPUEwMTY0NzU4U0NBV05GMktMRkpQJmVuY3J5cHRlZEFkSWQ9QTAxMTU5MDIxWlJOWlM3T0FaT0daJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=='

cop = ChromeOperate()
cop.open(item_url)
page = cop.driver.page_source
if 'Kindle Edition' in page:
    print(page)
item_info = extractor_page(page)
if 'Type the characters you see' in page  :
    print('IP被封了',url)
    time.sleep(10)
    # print page
item_info['keyword'] = '1'
item_info['rank'] = '2'
item_info['item_url'] = item_url.split('?')[0]
item_infos.append(item_info)

gen_xls(item_infos)