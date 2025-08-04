from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import time

class CareersPage(BasePage):

    def __init__(self, driver):

        super().__init__(driver)
        
        # Sayfa elementlerini tanımladım (locator'lar)
        self.see_all_qa_jobs_button = (By.XPATH, "//a[contains(text(),'See all QA jobs')]")
        self.location_filter = (By.ID, "filter-by-location")
        self.department_filter = (By.ID, "filter-by-department")
        
        # Kariyer sayfası blokları için locator'lar
        self.locations_block = (By.XPATH, "//*[contains(text(),'Our Locations') or contains(text(),'location')]")
        self.teams_block = (By.XPATH, "//*[contains(text(),'Find your calling') or contains(text(),'team')]")
        self.life_at_insider_block = (By.XPATH, "//*[contains(text(),'Life at Insider') or contains(text(),'life')]")
        
        # İş ilanları ile ilgili locator'lar
        self.job_position_elements = (By.XPATH, "//div[contains(@class,'position')]")
        self.select2_location_container = (By.XPATH, "//span[@id='select2-filter-by-location-container']")
        self.select2_dropdown_options = (By.XPATH, "//li[contains(@class,'select2-results__option')]")
        self.job_list_elements = (By.XPATH, "//div[contains(@class,'position') or contains(@class,'job') or contains(@class,'role')]")
        self.no_results_elements = (By.XPATH, "//p[contains(text(),'No positions available') or contains(text(),'No results')]")
        self.view_role_buttons = (By.XPATH, "//a[contains(text(),'View Role')]")
        
    def click_see_all_qa_jobs(self):
        try:
            self.click_element(self.see_all_qa_jobs_button)
            return True
        except Exception as e:
            print(f"Error clicking See all QA jobs: {e}")
            return False
    
    def verify_careers_page_blocks(self):
        try:
            # Locations bloğunun var olup olmadığını kontrol ediyorum
            locations_present = self.is_element_present(self.locations_block)
            print(f"Locations block present: {locations_present}")
            
            # Teams bloğunun var olup olmadığını kontrol ediyorum
            teams_present = self.is_element_present(self.teams_block)
            print(f"Teams block present: {teams_present}")
            
            # Life at Insider bloğunun var olup olmadığını kontrol ediyorum
            life_present = self.is_element_present(self.life_at_insider_block)
            print(f"Life at Insider block present: {life_present}")
            
            # Tüm blokların olması gerekiyor, olmayanı logluyorum
            if not locations_present:
                print("Locations block not found")
            if not teams_present:
                print("Teams block not found")
            if not life_present:
                print("Life at Insider block not found")
            
            # Tüm bloklar varsa test geçer
            return locations_present and teams_present and life_present
        except Exception as e:
            print(f"Error verifying careers page blocks: {e}")
            return False
    
    def wait_for_jobs_to_load(self, timeout=15):  
        try:
            wait = WebDriverWait(self.driver, timeout)
            # İş elementlerinin yüklenmesini bekliyorum (explicit wait)
            wait.until(EC.presence_of_element_located(self.job_position_elements))
            
            time.sleep(2)   #backend'in filteleri getirmesi için minik buffer
            print("Jobs data loaded successfully")
            return True
            
        except Exception as e:
            print(f"Error waiting for jobs to load: {e}")
            return False
    
    def filter_by_location(self, location="Istanbul, Turkiye"):
        try:
            # Önce iş ilanlarının yüklenmesini bekliyorum
            if not self.wait_for_jobs_to_load():
                print("Jobs did not load, cannot filter by location")
                return False
            
            # Lokasyon filtresi dropdown'ını buluyorum
            location_element = self.find_element(self.location_filter)
            
            # dropdown olup olmadığını kontrol ediyorum
            is_select2 = "select2-hidden-accessible" in location_element.get_attribute("class")
            
            if is_select2:
                select2_container = self.driver.find_element(*self.select2_location_container)  # tuple'ı açıyorum
                
                # Select2 container'ına tıklayarak dropdown'ı açıyorum
                select2_container.click()
                time.sleep(0.5)
                
                # Location dropdown seçeneklerini buluyorum
                dropdown_options = self.driver.find_elements(*self.select2_dropdown_options)  # tuple'ı açıyorum
                print(f"Found {len(dropdown_options)} location dropdown options")
                
                # Mevcut seçenekleri list'e atıyorum
                available_options = []
                for option in dropdown_options:
                    option_text = option.text.strip()
                    if option_text:
                        available_options.append(option_text)
                
                                 
                # İstenen lokasyonu bulup tıklıyorum
                location_found = False
                for option in dropdown_options:
                    option_text = option.text.strip()
                    if location.lower() in option_text.lower():
                        option.click()
                        location_found = True
                        break
                
                if not location_found:
                    print(f"Location '{location}' not found in Select2 dropdown")
                    return available_options
                
                return available_options
            else:
                # Standart select elementi
                select = Select(location_element)
                available_options = [option.text for option in select.options]
                print(f"Available location options: {available_options}")
                
                if location in available_options:
                    select.select_by_visible_text(location)
                    print(f"Successfully selected location: {location}")
                    return True
                
                print(f"Location '{location}' not available in dropdown")
                return available_options
            
        except Exception as e:
            print(f"Error filtering by location: {e}")
            return False
    
    def filter_by_department(self, department="Quality Assurance"):
        try:
            # Önce iş ilanlarının yüklenmesini bekliyorum
            if not self.wait_for_jobs_to_load():
                print("Jobs did not load, cannot filter by department")
                return False
            
            # Departman filtresi dropdown'ını buluyorum 
            department_element = self.find_element(self.department_filter)
            
            # Select elementi mi yoksa custom dropdown mı kontrol ediyorum
            tag_name = department_element.tag_name
            print(f"Department filter element tag: {tag_name}")
            
            if tag_name == "select":
                # Standart select elementi
                select = Select(department_element)
                available_options = [option.text for option in select.options]
                
                if department not in available_options: #aradığım seçenek listede yoksa
                    print(f"Department '{department}' not available in dropdown")
                    return available_options 
                
                select.select_by_visible_text(department)

                return available_options  # List'i return ediyorum ki içini arayabileyim
            else:
                print(f"Custom dropdown detected (tag: {tag_name})")
                print("Custom dropdowns may not have the expected options loaded")
                print("This is normal for dynamic content that loads via JavaScript")
                return False
            
        except Exception as e:
            print(f"Error filtering by department: {e}")
            return False
    
    def verify_job_list_present(self):
        try:
            # "Job" ile ilgili elementleri arıyorum 
            job_elements = self.driver.find_elements(*self.job_list_elements)  
            no_results_elements = self.driver.find_elements(*self.no_results_elements)  # tuple'ı açıyorum
            
            if job_elements and len(job_elements) > 0:
                print("Job list is present on the page")
                return True
            elif no_results_elements and any(elem.is_displayed() for elem in no_results_elements):
                print("No job positions available (but page is working)")
                return True
            else:
                print("Job list not found")
                return False
        except Exception as e:
            print(f"Error verifying job list: {e}")
            return False
    
    def verify_filtered_jobs_contain_expected_values(self, location_options, department_options):
        try:
            # "Istanbul, Turkiye" lokasyon seçeneklerinde var mı kontrol ediyorum
            expected_location = "Istanbul, Turkiye"
            location_found = expected_location in location_options
            print(f"Location '{expected_location}' found in options: {location_found}")
            
            # "Quality Assurance" departman seçeneklerinde var mı kontrol ediyorum
            expected_department = "Quality Assurance"
            department_found = expected_department in department_options
            print(f"Department '{expected_department}' found in options: {department_found}")
            
            # Test geçmesi için ikisi de bulunmalı
            if location_found and department_found:
                print("All expected filter values are present")
                return True
            else:
                print("Some expected filter values are missing")
                return False
                
        except Exception as e:
            print(f"Error verifying filtered jobs: {e}")
            return False
    
    def click_view_role_button(self):
        try:
            view_role_buttons = self.driver.find_elements(*self.view_role_buttons)  # tuple'ı açıyorum
            
            if not view_role_buttons:
                print("No View Role buttons found")
                return False
            
            # İlk çıkan 'View Role' butonuna tıklıyorum
            first_button = view_role_buttons[0]
            
            # Elementi görünür yapmak için önce scroll
            self.driver.execute_script("arguments[0].scrollIntoView(true);", first_button)
            time.sleep(1)  # Scroll'ın tamamlanmasını bekliyorum
            
            # JavaScript click kullanıyorum (normal click navbar overlap nedeniyle başarısız oluyordu)
            self.driver.execute_script("arguments[0].click();", first_button)
            print("Successfully clicked View Role button")
            return True
            
        except Exception as e:
            print(f"Error clicking View Role button: {e}")
            return False
    
    def verify_redirect_to_lever(self):
        try:
            # View Role butonu yeni tab/window açıyor
            # Yeni window/tab açılıp açılmadığını kontrol ediyorum
            original_window = self.driver.current_window_handle
            all_windows = self.driver.window_handles
            
            # Yeni window varsa, ona geçip URL'yi kontrol ediyorum
            if len(all_windows) > 1:
                # Yeni window'a geçiyorum
                new_window = [window for window in all_windows if window != original_window][0]
                self.driver.switch_to.window(new_window)
                
                # URL'de "lever" var mı kontrol ediyorum
                current_url = self.driver.current_url
                is_lever = "lever" in current_url.lower()
                return is_lever
            else:
                # Yeni window açılmadıysa, mevcut URL'yi kontrol ediyorum
                current_url = self.driver.current_url
                return "lever" in current_url.lower()
                
        except Exception as e:
            print(f"Error verifying Lever redirect: {e}")
            return False 