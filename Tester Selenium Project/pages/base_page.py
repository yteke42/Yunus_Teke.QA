from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class BasePage:

    def __init__(self, driver):
        self.driver = driver
        # Wait up to 10 seconds for elements to appear
        self.wait = WebDriverWait(driver, 10)
    
    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def find_clickable_element(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))
    
    def click_element(self, locator):
        element = self.find_clickable_element(locator)
        element.click()
    
    def is_element_present(self, locator):
        try:
            self.find_element(locator)
            return True
        except TimeoutException:
            return False
    
    def wait_for_page_title(self, title):
        self.wait.until(EC.title_contains(title))
    