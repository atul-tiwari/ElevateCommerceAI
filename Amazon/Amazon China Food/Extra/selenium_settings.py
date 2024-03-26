import platform
import traceback
import lxml.html
from amazoncaptcha import AmazonCaptcha
#from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from seleniumwire import webdriver
import requests,random

response = requests.get(f"https://proxy.webshare.io/api/v2/proxy/list/?mode=direct&page={random.randint(1,5)}&page_size=50", headers={"Authorization": "94a3056cb6e4d13ef5b61adbb44c8b99d2f9aef4"})
data_dict = response.json()
proxy_list = list(map(lambda x: f"http://{x['username']}:{x['password']}@{x['proxy_address']}:{x['port']}",data_dict['results']))


def get_Driver(proxy):
    
    pf = platform.system()
    if pf == 'Linux':
        DOWNLOAD_PATH = './download'
        # self.DOWNLOAD_PATH = str(os.path.abspath(os.getcwd())) + "/download/"
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument('--disable-dev-shm-usage')
        # options.add_argument("--remote-debugging-port=9222")
        options.add_argument("--no-sandbox")
        options.add_argument("lang=ja_JP")
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1280,1024')
        # userdata_dir = 'UserData'
        # options.add_argument("--user-data-dir=" + userdata_dir)
        # options.add_argument('--profile-directory=profile')
        # options.setExperimentalOption("useAutomationExtension", false)
        prefs = {"download.default_directory": DOWNLOAD_PATH , # pass the variable
                "download.prompt_for_download": False,
                "directory_upgrade": True,
                "safebrowsing.enabled": True }
        options.add_experimental_option("prefs",prefs)
        options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        try:
            driver = webdriver.Chrome("/bin/chromedriver", chrome_options=options)
        except Exception as e:
            print(e)

    elif pf == 'Darwin':
        downloadPath = './download'
        options = Options()
        # options.add_argument('--headless')
        # options.add_argument("--remote-debugging-port=9222")
        # options.add_argument("--disable-dev-shm-using")
        # options.add_argument("--disable-extensions")
        # options.add_argument("start-maximized")
        # options.add_argument("disable-infobars")
        # options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        # options.add_argument('--incognito')
        options.add_argument('--window-size=1600,1200')

        # https://qiita.com/ttn_tt/items/81d215683e7fbf0ebd81
        # https://stackoverflow.com/questions/34548041/selenium-give-file-name-when-downloading

        prefs = {
            "download.default_directory": os.path.abspath(downloadPath),
            "download.directory_upgrade": True,
            "'download.extensions_to_open'": '',
            "download.prompt_for_download": False,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)

        options.add_argument('--ignore-certificate-errors')  # SSLエラー対策
        driver = webdriver.Chrome("/usr/local/bin/chromedriver", options=options)

    elif pf == 'Windows':
        #cx_Oracle.init_oracle_client(lib_dir= r"C:\instantclient_21_3")
        options = Options()
        options.add_argument('--headless')
        # options.add_argument("--remote-debugging-port=9222")
        # options.add_argument("--disable-dev-shm-using")
        # options.add_argument("--disable-extensions")
        # options.add_argument("start-maximized")
        # options.add_argument("disable-infobars")
        # options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        # options.add_argument('--incognito')
        options.add_argument('--window-size=1280,1024')
        prefs = {"download.prompt_for_download": False,
                "directory_upgrade": True,
                "safebrowsing.enabled": True,
                "profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs",prefs)

        options.add_argument(f'--proxy-server={random.choice(proxy_list)}')
        options.add_argument('--ignore-certificate-errors')  # SSLエラー対策
        driver = webdriver.Chrome(options=options)
        
        driver.set_page_load_timeout(5)
        return driver


def selenium_get_dom(driver,URL):
    retries = 1
    while retries <= 5:
        driver.get(URL)
        try:
            #captcha Check 
            dom = lxml.html.fromstring(driver.page_source)
            if dom.xpath("boolean(//h4[contains(.,'请输入您在这个图片中看到的字符')])") == 1:
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
            wait.until(EC.presence_of_element_located((By.XPATH, "//a[@id='bylineInfo']")))

            break
        except :
            print("Retry")
            driver.refresh()
            retries += 1

    HTML = driver.page_source
    return lxml.html.fromstring(HTML)