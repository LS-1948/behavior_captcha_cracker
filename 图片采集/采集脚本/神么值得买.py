import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_chorme():
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(options=options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})""",
    })

    driver.maximize_window()

    driver.get('https://www.smzdm.com/')

    return driver

def save(driver):
    while True:
        element = driver.find_element_by_xpath(
            '/html/body/div[3]/div[2]/div[6]/div/div[1]/div[1]/div/a/div[1]/div/canvas[2]')
        filename = str(str(int(time.time())) + '.png')
        scrrenshot = element.screenshot_as_png
        with open(filename, 'wb') as f:
            f.write(scrrenshot)
        refreash(driver)
        time.sleep(2)

def refreash(driver):
    try:
        driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[6]/div/div[2]/div/a[2]').click()
    except Exception as e:
        print(e)

def clicklogin(driver):
    driver.find_element_by_xpath('//*[@id="login_submit"]').click()

def tool(driver):
    i = 1
    while i < 10:
        try:
            save(driver)
        except Exception as e:
            driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[4]/div[3]').click()
            time.sleep(5)
            save(driver)
            print(e)
        finally:
            tool(driver)

def show_login(driver):
    try:
        driver.find_element_by_xpath('//*[@id="global-nav"]/div/div/span/a[1]').click()
        driver.implicitly_wait(10)
        driver.switch_to.frame('J_login_iframe')
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/div[1]/div[1]').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="username"]').send_keys('13105504542')
        driver.find_element_by_xpath('//*[@id="password"]').send_keys('13105504542')
        driver.find_element_by_xpath('//*[@id="login_submit"]').click()
        driver.implicitly_wait(10)

        flag = tool(driver)

        while flag:
            tool(driver)
            continue

    except Exception as e:
        print(e)

def driver_quit(driver):
    try:
        driver.close()
        driver.quit()
    except Exception as e:
        print(e)
        driver.quit()


if __name__ == '__main__':
    driver = get_chorme()
    show_login(driver)
    driver_quit(driver)