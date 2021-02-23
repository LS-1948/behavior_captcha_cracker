import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = webdriver.Chrome(options=options)

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})""",
})


def save(element):
    filename = str(str(int(time.time())) + '.png')
    scrrenshot = element.screenshot_as_png
    with open(filename, 'wb') as f:
        f.write(scrrenshot)


try:
    driver.maximize_window()
    driver.get('https://www.geetest.com/Sensebot')
    driver.implicitly_wait(20)
    driver.find_element_by_xpath('//*[@id="gt-sensebot-mobile"]/div[2]/section[3]/div/div[2]/div[1]/ul/li[2]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="captcha"]/div[3]/div[2]').click()
    element = driver.find_element_by_xpath(
        '/html/body/div[3]/div[2]/div[1]/div/div[1]/div[1]/div/a/div[1]/div/canvas[2]')
    save(element)
    i = 0
    while i < 100:
        driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div/div[2]/div/a[2]').click()
        driver.implicitly_wait(30)
        time.sleep(2)
        try:
            element = driver.find_element_by_xpath(
                '/html/body/div[3]/div[2]/div[1]/div/div[1]/div[1]/div/a/div[1]/div/canvas[2]')
            save(element)
            i = i + 1
            time.sleep(5)
        except Exception as e:
            driver.find_element_by_xpath('//*[@id="captcha"]/div[3]/div[2]/div[1]/div[3]/span[2]').click()
            driver.implicitly_wait(30)
            time.sleep(2)
    # input('结束程序')
    driver.close()
    driver.quit()

except Exception as e:
    print(e)
    driver.close()
    driver.quit()
