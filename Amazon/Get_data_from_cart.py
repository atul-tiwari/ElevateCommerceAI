import lxml.html
from Amazon import selenium_get_dom
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

def get_amazon_cart(driver):
    
    cart_page_url = "https://www.amazon.com/gp/cart/view.html?ref_=nav_cart"

    dom,driver = selenium_get_dom(driver,cart_page_url)

    products_list = dom.xpath("//div[@data-name='Active Items']/div/@data-asin")

    print(products_list)

    for i in range (len(products_list)):
        try:
            driver.find_element(By.XPATH,"//span[@id='a-autoid-1-announce']").click()
            driver.find_element(By.XPATH,"//a[@id='quantity_0']").click()

            driver.refresh()
        except:
            pass
        