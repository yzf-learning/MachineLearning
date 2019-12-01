# encoding: utf-8  



""" 

@author: Meng.ZhiHao 

@contact: 312141830@qq.com 

@file: selenium_operate.py 

@time: 2018/1/29 11:42 

"""

import selenium

import os

from selenium import webdriver

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.action_chains import ActionChains



#文档https://www.cnblogs.com/taceywong/p/6602927.html?utm_source=tuicool&utm_medium=referral



#中文apihttp://selenium-python-zh.readthedocs.io/en/latest/

class ChromeOperate():

    def __init__(self,url='',executable_path='',User_data_dir='',arguments=[]):

        option = webdriver.ChromeOptions()

        if User_data_dir:

            option.add_argument( '--user-data-dir=%s'%User_data_dir)  # 设置成用户自己的数据目录

        else:

            import getpass

            username = getpass.getuser()

            default_path = r'C:\Users\%s\AppData\Local\Google\Chrome\User Data'%username  #echo %LOCALAPPDATA%\Google\Chrome\User Data

            if os.path.exists(default_path):

                # option.add_argument('--user-data-dir=%s' % default_path)

                pass

        option.add_argument('--start-maximized')

        #option.add_argument('headless')

        option.add_argument('google-base-url=%s' % 'https://www.baidu.com/')

        for argument in arguments:

            option.add_argument(argument)

        if not executable_path:executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'

        self.driver = webdriver.Chrome(executable_path=executable_path,chrome_options=option)



        if url:self.open(url)





    def open(self,url):

        self.driver.get(url) #   self.driver.get(url).page_source



    def open_source(self):

        return self.driver.page_source



    def title(self):

        self.title=self.driver.title

        return self.title



    def quit(self):

        self.driver.quit()



    def find_element_by_name(self,name):

        return self.driver.find_element_by_name(name)



    def find_elements_by_xpath(self,xpath): #貌似不能用/text

        return self.driver.find_elements_by_xpath(xpath)



    def find_element_by_id(self,id):

        try:

            return self.driver.find_element_by_id(id)

        except:

            return None



    def input_words(self,element,words):

        element.clear()

        element.send_keys(words)



    def click_by_id(self,id):

        self.driver.find_element_by_id(id).click()



    def send_file(self,element,path):

        element.sendKeys(path);



    def wait_element(self,element_id):

        WebDriverWait(self.driver, 10).until(

            EC.presence_of_element_located((By.ID, element_id))

        )



    def get_title(self):

        print(self.driver.title)

        return self.driver.title



    def refresh(self):

        self.driver.refresh()  #



    def down_page(self):

        from selenium.webdriver.common.keys import Keys

        self.driver.execute_script("window.scrollBy(0,3000)")



    def get_cookie(self):

        cookies = self.driver.get_cookies()

        return cookies



    def download_chrome_driver(self):

        pass





'''

验证码截取

链式操作ActionChains(driver).move_to_element(menu).click(hidden_submenu).perform()



// Copy the element screenshot to disk

File screenshotLocation = new File("C:\\images\\GoogleLogo_screenshot.png");

FileUtils.copyFile(screenshot, screenshotLocation);



'''



if __name__ == '__main__':

    cop = ChromeOperate(executable_path=r'chromedriver.exe')

    import time

    cop.open("https://e.ikcrm.com/spa#/customers")

    account = cop.find_element_by_id('account')

    cop.input_words(account,'13064766048')

    password = cop.find_element_by_id('password')

    cop.input_words(password,'Test1234')

    time.sleep(1)

    cop.driver.find_element_by_xpath('//button').click()

    time.sleep(3)

    cop.open("https://e.ikcrm.com/spa#/customers")

    time.sleep(3)

    with open('1.html','w',encoding='utf-8') as f:

        page_buf = cop.open_source()

        f.write(page_buf)

        print(page_buf)

    cop.quit()

    #c9a04bcd-5e9b-ee39-a803-7d8bd15dcd06





# hqfEP09&

# hunqi07433yanz@163.com