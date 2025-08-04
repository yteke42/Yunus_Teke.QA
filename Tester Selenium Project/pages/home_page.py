from selenium.webdriver.common.by import By
from .base_page import BasePage

class HomePage(BasePage):
    
    def __init__(self, driver):

        super().__init__(driver)
        
        # Sayfa elementlerini tanımlıyorum (locator'lar)
        self.company_menu = (By.XPATH, "//a[contains(text(),'Company')]") #xpath kullandım
        self.careers_link = (By.XPATH, "//a[contains(text(),'Careers')]")
        self.page_title = "#1 Leader in Individualized, Cross-Channel CX — Insider"
    

    def click_company_menu(self):
        try:
            self.click_element(self.company_menu)
            return True
        except Exception as e:
            print(f"Error clicking Company menu: {e}")
            return False
    
    def click_careers_link(self):
        try:
            self.click_element(self.careers_link)
            return True
        except Exception as e:
            print(f"Error clicking Careers link: {e}")
            return False
    
    def is_homepage_loaded(self):
        try:
            return self.is_element_present(self.company_menu)
        except Exception as e:
            print(f"Error checking homepage load: {e}")
            return False
    
    def get_page_title(self):
        return self.driver.title 
    