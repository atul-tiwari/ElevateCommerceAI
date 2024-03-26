from Amazon_Scraper import get_category_data
from selenium_settings import get_Driver
from time import sleep
import pickle

category_list = [
"https://www.amazon.cn/s?rh=n%3A2141094051&fs=true&ref=lp_2141094051_sar",
"https://www.amazon.cn/s?rh=n%3A2140457051&fs=true&ref=lp_2140457051_sar",
"https://www.amazon.cn/s?rh=n%3A43234071&fs=true&ref=lp_43234071_sar",
"https://www.amazon.cn/s?rh=n%3A2141095051&fs=true&ref=lp_2141095051_sar",
"https://www.amazon.cn/s?rh=n%3A2134633051&fs=true&ref=lp_2134633051_sar",
"https://www.amazon.cn/s?rh=n%3A2134644051&fs=true&ref=lp_2134644051_sar",
"https://www.amazon.cn/s?rh=n%3A2134651051&fs=true&ref=lp_2134651051_sar",
"https://www.amazon.cn/s?rh=n%3A1844461071&fs=true&ref=lp_1844461071_sar",
"https://www.amazon.cn/s?rh=n%3A2134669051&fs=true&ref=lp_2134669051_sar",
"https://www.amazon.cn/s?rh=n%3A2134670051&fs=true&ref=lp_2134670051_sar",
"https://www.amazon.cn/s?rh=n%3A2134675051&fs=true&ref=lp_2134675051_sar",
"https://www.amazon.cn/s?rh=n%3A2134680051&fs=true&ref=lp_2134680051_sar",
"https://www.amazon.cn/s?rh=n%3A2134691051&fs=true&ref=lp_2134691051_sar",
"https://www.amazon.cn/s?rh=n%3A2134701051&fs=true&ref=lp_2134701051_sar",
"https://www.amazon.cn/b?node=2134729051&ref=lp_2127216051_nr_n_14",
"https://www.amazon.cn/s?rh=n%3A1538296071&fs=true&ref=lp_1538296071_sar"
]

if __name__ == '__main__':


    index = 1
    for category in category_list:
        driver = get_Driver()
        driver.minimize_window()
        
        
        data = get_category_data(driver,category)

        data = {"category_name":index,"category_url":category,"data":data}
        file = open(f'{ (data["category_name"]) }.pickle', 'wb')
        pickle.dump(data, file)
        file.close()
    

        driver.close()
        driver.quit()
        index+=1