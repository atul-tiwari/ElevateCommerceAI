import lxml.html
from amazoncaptcha import AmazonCaptcha

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def selenium_get_dom(driver,URL,check = "//body"):
    retries = 1
    while retries <= 5:
        driver.get(URL)
        try:
            #captcha Check 
            dom = lxml.html.fromstring(driver.page_source)
            if dom.xpath("boolean(//h4[contains(.,'Enter the characters you see below')])") == 1:
                captcha_img_url=dom.xpath("//img[contains(@src,'.jpg')]/@src")[0]
                captcha = AmazonCaptcha.fromlink(captcha_img_url)
                solution = captcha.solve()
                captcha_filed = driver.find_element(By.XPATH,"//input[@id='captchacharacters']")
                captcha_filed.send_keys(solution)
                driver.find_element(By.XPATH,"//button[@type='submit']").click()
                print("captcha = ",solution)
            cookies = driver.get_cookies()
            for cookie in cookies:
                driver.add_cookie(cookie)

            wait = WebDriverWait(driver, 4)
            wait.until(EC.presence_of_element_located((By.XPATH,check)))

            break
        except :
            print("Retry")
            driver.refresh()
            retries += 1

    HTML = driver.page_source
    dom = lxml.html.fromstring(HTML)
    return dom, driver