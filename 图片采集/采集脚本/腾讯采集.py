import json
import random
import sqlite3
import time
import requests
from requests.cookies import RequestsCookieJar
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait  # WebDriverWait注意大小写
from selenium.webdriver.common.by import By

class QianKuParse:
    def __init__(self):
        print('初始化千库网')
        pass
    def __del__(self):
        print('销毁千库网实例')
        self.driver.close()
        self.driver.quit()
        pass

    def get_driver(self):
        self.options = Options()
        # self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('lang=zh_CN.UTF-8')
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})""",
        })
        self.driver.maximize_window()
        self.driver.get('https://588ku.com/')

    def find_element_xpath(self, xpath, tips):
        locator = (By.XPATH, xpath)
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator), '未找到' + tips)
        return element

    def yzm(self):
        element = self.find_element_xpath('//*[@id="tcOperation"]/div[1]/div[1]', '验证码')
        filename = str(str(int(time.time())) + '.png')
        scrrenshot = element.screenshot_as_png
        with open(filename, 'wb') as f:
            f.write(scrrenshot)
        self.refreash()
        time.sleep(2)

    def refreash(self):
        self.find_element_xpath('//*[@id="guideWrap"]/div/div[1]','刷新按钮').click()


    def login(self):
        self.get_driver()
        self.find_element_xpath('//*[@id="top-click"]/ul/li[5]/div/a','登录按钮').click()
        time.sleep(5)
        self.find_element_xpath('/html/body/div[9]/div[2]/div[3]/a[1]','QQ登录').click()
        time.sleep(5)
        # 当前主窗口
        main_handle = self.driver.current_window_handle
        # 获取所有窗口句柄
        all_handles = self.driver.window_handles
        # 弹出两个界面,跳转到不是主窗体界面
        for handle in all_handles:
            if handle != main_handle:
                # 输出待选择的窗口句柄
                print('当前窗口句柄：' + handle)
                self.driver.switch_to.window(handle)
                self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                    "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})""",
                })

                print('弹出界面信息')
                print('弹出窗口URL：' + self.driver.current_url)
                print('弹出窗口标题：' + self.driver.title)

                self.driver.switch_to.frame('ptlogin_iframe')
                self.find_element_xpath('//*[@id="switcher_plogin"]', '账号密码登录').click()
                self.find_element_xpath('//*[@id="u"]', '账号输入框').send_keys("34656034")
                # self.find_element_xpath('//*[@id="u"]', '账号输入框').send_keys(self.user)
                self.find_element_xpath('//*[@id="p"]', '密码输入框').send_keys("lvshuo1234")
                # self.find_element_xpath('//*[@id="p"]', '密码输入框').send_keys(self.passwd)
                time.sleep(0.2)
                self.find_element_xpath('//*[@id="login_button"]', '登录按钮').click()
                time.sleep(10)
                self.driver.switch_to.frame(self.find_element_xpath('//*[@id="tcaptcha_iframe"]', '验证码'))
                while True:
                    try:
                        self.yzm()
                    except Exception as e:
                        # self.refreash()
                        pass
                    finally:
                        self.yzm()

if __name__ == '__main__':
    qianku = QianKuParse()
    qianku.login()

    del qianku
