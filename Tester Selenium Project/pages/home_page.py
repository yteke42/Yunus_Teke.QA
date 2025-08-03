from selenium.webdriver.common.by import By
from .base_page import BasePage

class HomePage(BasePage):
    """
    Home page class for Insider website.
    Contains methods to interact with the homepage elements.
    """
    
    def __init__(self, driver):
        """
        Initialize the home page with webdriver.
        
        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)
        
        # Define page elements (locators)
        # These are the ways to find elements on the page
        self.company_menu = (By.XPATH, "//a[contains(text(),'Company')]") #I used the xpath
        self.careers_link = (By.XPATH, "//a[contains(text(),'Careers')]")
        self.page_title = "#1 Leader in Individualized, Cross-Channel CX — Insider"
    
    def navigate_to_homepage(self):
        """
        Navigate to the Insider homepage.
        
        Returns:
            bool: True if navigation successful
        """
        try:
            self.driver.get("https://useinsider.com/")
            self.wait_for_page_title(self.page_title)
            return True
        except Exception as e:
            print(f"Error navigating to homepage: {e}")
            return False
    
    def click_company_menu(self):
        """
        Click on the Company menu in the navigation bar.
        
        Returns:
            bool: True if click successful
        """
        try:
            self.click_element(self.company_menu)
            return True
        except Exception as e:
            print(f"Error clicking Company menu: {e}")
            return False
    
    def click_careers_link(self):
        """
        Click on the Careers link in the Company menu.
        
        Returns:
            bool: True if click successful
        """
        try:
            self.click_element(self.careers_link)
            return True
        except Exception as e:
            print(f"Error clicking Careers link: {e}")
            return False
    
    def is_homepage_loaded(self):
        """
        Check if the homepage is properly loaded.
        
        Returns:
            bool: True if homepage elements are present
        """
        try:
            # Check if Company menu is present
            return self.is_element_present(self.company_menu)
        except Exception as e:
            print(f"Error checking homepage load: {e}")
            return False
    
    def get_page_title(self):
        """
        Get the current page title.
        
        Returns:
            str: Page title
        """
        return self.driver.title 