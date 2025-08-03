from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class BasePage:
    """
    Base page class that contains common methods for all page objects.
    This is the foundation of our Page Object Model (POM).
    """
    
    def __init__(self, driver):
        """
        Initialize the base page with a webdriver instance.
        
        Args:
            driver: WebDriver instance (Chrome, Firefox, etc.)
        """
        self.driver = driver
        # Wait up to 10 seconds for elements to appear
        self.wait = WebDriverWait(driver, 10)
    
    def find_element(self, locator):
        """
        Find an element on the page with explicit wait.
        
        Args:
            locator: Tuple of (By, value) - e.g., (By.ID, "username")
        
        Returns:
            WebElement: The found element
        """
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def find_clickable_element(self, locator):
        """
        Find an element that can be clicked with explicit wait.
        
        Args:
            locator: Tuple of (By, value)
        
        Returns:
            WebElement: The clickable element
        """
        return self.wait.until(EC.element_to_be_clickable(locator))
    
    def click_element(self, locator):
        """
        Click on an element with explicit wait.
        
        Args:
            locator: Tuple of (By, value)
        """
        element = self.find_clickable_element(locator)
        element.click()
    
    def send_keys_to_element(self, locator, text):
        """
        Type text into an element with explicit wait.
        
        Args:
            locator: Tuple of (By, value)
            text: Text to type
        """
        element = self.find_element(locator)
        element.clear()  # Clear existing text
        element.send_keys(text)
    
    def get_element_text(self, locator):
        """
        Get text from an element.
        
        Args:
            locator: Tuple of (By, value)
        
        Returns:
            str: Text from the element
        """
        element = self.find_element(locator)
        return element.text
    
    def is_element_present(self, locator):
        """
        Check if an element is present on the page.
        
        Args:
            locator: Tuple of (By, value)
        
        Returns:
            bool: True if element is present, False otherwise
        """
        try:
            self.find_element(locator)
            return True
        except TimeoutException:
            return False
    
    def wait_for_page_title(self, title):
        """
        Wait for page title to contain specific text.
        
        Args:
            title: Text to look for in page title
        """
        self.wait.until(EC.title_contains(title))
    
    def get_page_title(self):
        """
        Get the current page title.
        
        Returns:
            str: Page title
        """
        return self.driver.title 