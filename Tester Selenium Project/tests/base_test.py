import unittest
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

class BaseTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Chrome seçeneklerini yapılandırıyorum
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        
        # Console uyarılarını bastırıyorum çünkü console'um çığlık atıyordu
        chrome_options.add_argument("--log-level=3")  
        chrome_options.add_argument("--silent")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-features=TranslateUI")
        chrome_options.add_argument("--disable-ipc-flooding-protection")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # WebDriver'ı başlatıyorum
        try:
            cls.driver = webdriver.Chrome(options=chrome_options)
        except Exception as e:
            print(f"Error initializing Chrome driver: {e}")
        
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()
    
    @classmethod
    def tearDownClass(cls):
        #Tüm testlerden sonra bir kez çalışır. Browser'ı kapatır
        if hasattr(cls, 'driver'):
            cls.driver.quit()
    
    def setUp(self):
        #Testten önce ana sayfaya gidiyorum.
        self.driver.get("https://useinsider.com/")
    
    def tearDown(self):
        #Her test metodundan sonra Cookie'leri ve local storage'ı temizliyorum.
        self.driver.delete_all_cookies()
        self.driver.execute_script("window.localStorage.clear();")
        self.driver.execute_script("window.sessionStorage.clear();")
    
    def take_screenshot(self, name):
        # Test başarısız olursa screenshot alıyorum.
        try:
            screenshot_path = f"screenshots/{name}.png"
            os.makedirs("screenshots", exist_ok=True)
            self.driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")
        except Exception as e:
            print(f"Error taking screenshot: {e}") 