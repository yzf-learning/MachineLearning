# -*- coding: utf-8 -*-

"""

File Name：     crawl_tool_for_py3

Description :

Author :       meng_zhihao

date：          2018/11/20



"""



import requests

from lxml import etree

import re

import datetime

HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}



#通用方法

class crawlerTool:



    def __init__(self):

        self.session = requests.session()

        pass



    def __del__(self):

        self.session.close()



    @staticmethod

    def get(url,proxies=None, cookies={}, referer=''):

        if referer:

            headers = {'Referer': referer}

            headers.update(HEADERS)

        else:

            headers = HEADERS

        rsp = requests.get(url, timeout=10, headers=headers, cookies=cookies)

        return rsp.content  # 二进制返回



    @staticmethod

    def post(url,data):

        rsp = requests.post(url,data,timeout=10)

        return rsp.content





    def sget(self,url,cookies={}):

        rsp = self.session.get(url,timeout=10,headers=HEADERS,cookies=cookies)

        return rsp.content # 二进制返回



    def spost(self,url,data):

        rsp = self.session.post(url,data,timeout=10,headers=HEADERS)

        return rsp.content







    # 获取xpath 要判断一下输入类型，或者异常处理

    @staticmethod

    def getXpath(xpath, content):   #xptah操作貌似会把中文变成转码&#xxxx;  /text()变unicode编码

        """



        :param xpath:

        :param content:

        :return:

        """

        tree = etree.HTML(content)

        out = []

        results = tree.xpath(xpath)

        for result in results:

            if  'ElementStringResult' in str(type(result)) or 'ElementUnicodeResult' in str(type(result)) :

                out.append(result)

            else:

                out.append(etree.tostring(result,encoding = "utf8",method = "html"))

        return out



    def getXpath1(xpath, content):   #xptah操作貌似会把中文变成转码&#xxxx;  /text()变unicode编码

        tree = etree.HTML(content)

        out = []

        results = tree.xpath(xpath)

        for result in results:

            if 'ElementStringResult' in str(type(result)) or 'ElementUnicodeResult' in str(type(result)):

                out.append(result)

            else:

                out.append(etree.tostring(result, encoding="utf8", method="html"))

        if out:

            return out[0]

        else:

            return ''



    @staticmethod

    def getRegex(regex, content):

        rs = re.search(regex,content)

        if rs:

            return rs.group(1)

        else:

            return ''


def img_resize(infile,outfile):
    im = Image.open(infile)
    # (x, y) = im.size  # read image size
    x_s = 120  # define standard width
    y_s = 160  # calc height based on standard width
    out = im.resize((x_s, y_s), Image.ANTIALIAS)  # resize image with high-quality
    out.save(outfile)


if __name__ == '__main__':

    content = crawlerTool.get('https://images-na.ssl-images-amazon.com/images/I/51QcRmb89wL._SX425_.jpg')

    #content = (content.decode('utf8'))
    file_path='1.jpg'
    with open(file_path, 'wb') as f:
            f.write(content)
            f.close()
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    book = xlsxwriter.Workbook('amazon%s.xlsx'%timestamp)
    worksheet = book.add_worksheet('demo')
    worksheet.set_column('A:D', 15) # 列宽约等于8像素 行高约等于1.37像素
    worksheet.set_column('C:C', 20)
    worksheet.set_column('B:B', 10)
    worksheet.set_column('F:F', 50)
    
    worksheet.set_row(0, 150)
    
    img_resize('1.jpg', 'img/tmp1.jpg')
    worksheet.insert_image( 0,2, 'img/tmp1.jpg',{'positioning': 1})
    book.close()
    #print(content)

