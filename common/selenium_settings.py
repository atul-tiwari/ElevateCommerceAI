import platform
import traceback
import requests,random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def get_Driver(proxy):
    
    pf = platform.system()
    if pf == 'Linux':
        DOWNLOAD_PATH = './download'
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--no-sandbox")
        options.add_argument("lang=ja_JP")
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1280,1024')
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
        driver = webdriver.Chrome(options=options)
        
        driver.set_page_load_timeout(5)
        return driver