from Amazon import selenium_get_dom
from selenium.webdriver.common.by import By
import time
from get_prod_details import get_dom_product_page
from common.selenium_settings import get_Driver

def login(Email, Password):
    login_url = 'https://www.amazon.com/'    

    driver = get_Driver(1)
    #driver.get(login_url)
    dom, driver = selenium_get_dom(driver,login_url)
    login_url = dom.xpath("//div[@id='nav-flyout-ya-signin']/a/@href")[0]

    dom, driver = selenium_get_dom(driver,login_url)

    Email_field = driver.find_element(By.XPATH,"//input[@id='ap_email']")
    Email_field.send_keys(Email)

    driver.find_element(By.XPATH,"//input[@id='continue']").click()

    pass_field = driver.find_element(By.XPATH,"//input[@id='ap_password']")
    pass_field.send_keys(Password)

    driver.find_element(By.XPATH,"//input[@id='signInSubmit']").click()

    return driver

def logout(driver):

    print()
    driver.find_element(By.XPATH,"//a[@id='nav-item-signout']/span").click()
    time.sleep(5)


driver = login('krishna056rocks@gmail.com','Piyush17#')
from Amazon.Get_data_from_cart import get_amazon_cart
asin_list,url_list=get_amazon_cart(driver)
for _url in url_list:
    get_dom_product_page (driver,_url)
logout(driver)