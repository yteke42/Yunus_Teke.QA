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
    """
    Base test class that provides common setup and teardown methods.
    All test classes should inherit from this class.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Set up test class - runs once before all tests.
        Initializes the WebDriver with Chrome browser.
        """
        # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        
        # Suppress console warnings and logging
        chrome_options.add_argument("--log-level=3")  # Only show fatal errors
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
        
        # Initialize WebDriver
        try:
            cls.driver = webdriver.Chrome(options=chrome_options)
        except Exception as e:
            print(f"Error initializing Chrome driver: {e}")
        
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()
    
    @classmethod
    def tearDownClass(cls):
        """
        Clean up test class - runs once after all tests.
        Closes the browser.
        """
        if hasattr(cls, 'driver'):
            cls.driver.quit()
    
    def setUp(self):
        """
        Set up each test method.
        Navigate to the homepage before each test.
        """
        self.driver.get("https://useinsider.com/")
    
    def tearDown(self):
        """
        Clean up after each test method.
        Clear cookies and local storage.
        """
        self.driver.delete_all_cookies()
        self.driver.execute_script("window.localStorage.clear();")
        self.driver.execute_script("window.sessionStorage.clear();")
    
    def take_screenshot(self, name):
        """
        Take a screenshot if test fails.
        
        Args:
            name: Name for the screenshot file
        """
        try:
            screenshot_path = f"screenshots/{name}.png"
            os.makedirs("screenshots", exist_ok=True)
            self.driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")
        except Exception as e:
            print(f"Error taking screenshot: {e}") 