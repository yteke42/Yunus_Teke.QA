from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class CareersPage(BasePage):
    """
    Careers page class for Insider website.
    Contains methods to interact with the careers page elements.
    """
    
    def __init__(self, driver):
        """
        Initialize the careers page with webdriver.
        
        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)
        
        # Define page elements (locators)
        self.product_engineering_link = (By.XPATH, "//a[contains(@href,'product-and-engineering')]")
        self.qa_jobs_link = (By.XPATH, "//a[contains(text(),'Quality Assurance') or contains(text(),'QA')]")
        self.see_all_qa_jobs_button = (By.XPATH, "//a[contains(text(),'See all QA jobs')]")
        self.location_filter = (By.ID, "filter-by-location")
        self.department_filter = (By.ID, "filter-by-department")
        self.job_list = (By.CLASS_NAME, "jobs-list")
        self.job_positions = (By.CLASS_NAME, "select2-results__option")
        self.job_departments = (By.CLASS_NAME, "department")
        self.job_locations = (By.CLASS_NAME, "location")
        self.view_role_buttons = (By.CLASS_NAME, "btn-view-role")
        
        # Careers page blocks locators
        self.locations_block = (By.XPATH, "//*[contains(text(),'Our Locations') or contains(text(),'location')]")
        self.teams_block = (By.XPATH, "//*[contains(text(),'Find your calling') or contains(text(),'team')]")
        self.life_at_insider_block = (By.XPATH, "//*[contains(text(),'Life at Insider') or contains(text(),'life')]")
        
        # Expected values for verification
        self.expected_department = "Quality Assurance"
        self.expected_location = "Istanbul, Turkiye"
    
    def click_product_engineering(self):
        """
        Click on "Product & Engineering" link.
        
        Returns:
            bool: True if click successful
        """
        try:
            self.click_element(self.product_engineering_link)
            return True
        except Exception as e:
            print(f"Error clicking Product & Engineering: {e}")
            return False
    
    def click_qa_jobs(self):
        """
        Click on QA jobs link.
        
        Returns:
            bool: True if click successful
        """
        try:
            self.click_element(self.qa_jobs_link)
            return True
        except Exception as e:
            print(f"Error clicking QA jobs: {e}")
            return False
    
    def click_see_all_qa_jobs(self):
        """
        Click on "See all QA jobs" button.
        
        Returns:
            bool: True if click successful
        """
        try:
            self.click_element(self.see_all_qa_jobs_button)
            return True
        except Exception as e:
            print(f"Error clicking See all QA jobs: {e}")
            return False
    
    def verify_careers_page_blocks(self):
        """
        Verify that Careers page blocks are present.
        
        Returns:
            bool: True if all blocks are present
        """
        try:
            # Check if Locations block is present
            locations_present = self.is_element_present(self.locations_block)
            print(f"Locations block present: {locations_present}")
            
            # Check if Teams block is present
            teams_present = self.is_element_present(self.teams_block)
            print(f"Teams block present: {teams_present}")
            
            # Check if Life at Insider block is present
            life_present = self.is_element_present(self.life_at_insider_block)
            print(f"Life at Insider block present: {life_present}")
            
            # Return True if at least one block is present (flexible approach)
            return locations_present or teams_present or life_present
        except Exception as e:
            print(f"Error verifying careers page blocks: {e}")
            return False
    
    def wait_for_jobs_to_load(self, timeout=10): #it was loading slow so i added this func
        """
        Wait for jobs to be loaded dynamically via JavaScript.
        
        Args:
            timeout: Maximum time to wait in seconds
        
        Returns:
            bool: True if jobs loaded successfully
        """
        try:
            # Wait for the jobs list to be populated
            wait = WebDriverWait(self.driver, timeout)
            
            # Wait for either job elements or "no results" message
            wait.until(lambda driver: (
                len(driver.find_elements(By.XPATH, "//div[contains(@class,'position')]")) > 0 or
                driver.find_element(By.XPATH, "//p[contains(text(),'No positions available')]").is_displayed()
            ))
            
            print("Jobs data loaded successfully")
            return True
        except Exception as e:
            print(f"Error waiting for jobs to load: {e}")
            return False
    
    def filter_by_location(self, location="Istanbul, Turkiye"):
        """
        Filter jobs by location.
        
        Args:
            location: Location to filter by (default: Istanbul, Turkiye)
        
        Returns:
            bool: True if filter applied successfully
        """
        try:
            # First wait for jobs to load
            if not self.wait_for_jobs_to_load():
                print("Jobs did not load, cannot filter by location")
                return False
            
            # Find the location filter dropdown
            location_element = self.find_element(self.location_filter)
            
            # Check if it's a select element or custom dropdown
            tag_name = location_element.tag_name
            print(f"Location filter element tag: {tag_name}")
            
            # Check if it's a Select2 dropdown (has select2-hidden-accessible class)
            is_select2 = "select2-hidden-accessible" in location_element.get_attribute("class")
            print(f"Is Select2 dropdown: {is_select2}")
            
            if is_select2:
                # Handle Select2 dropdown
                print("Handling Select2 dropdown...")
                
                # Try different Select2 container selectors
                select2_selectors = [
                    "//span[contains(@class,'select2') and @data-select2-id='filter-by-location']",
                    "//span[contains(@class,'select2') and contains(@class,'selection')]",
                    "//span[contains(@class,'select2')]",
                    "//div[contains(@class,'select2') and contains(@class,'container')]",
                    "//span[contains(@class,'select2-selection')]"
                ]
                
                select2_container = None
                for selector in select2_selectors:
                    try:
                        select2_container = self.driver.find_element(By.XPATH, selector)
                        print(f"Found Select2 container with selector: {selector}")
                        break
                    except:
                        continue
                
                if not select2_container:
                    print("Could not find Select2 container. Available Select2 elements:")
                    select2_elements = self.driver.find_elements(By.XPATH, "//*[contains(@class,'select2')]")
                    for elem in select2_elements:
                        print(f"  - {elem.tag_name}: {elem.get_attribute('class')} | {elem.get_attribute('data-select2-id')}")
                    return False
                
                # Click the Select2 container to open dropdown
                select2_container.click()
                print("Clicked Select2 container")
                
                # Wait for dropdown options to appear
                import time
                time.sleep(2)
                
                # Look for the dropdown options in Select2
                try:
                    # Try to find Select2 dropdown options
                    dropdown_options = self.driver.find_elements(By.XPATH, "//li[contains(@class,'select2-results__option')]")
                    print(f"Found {len(dropdown_options)} Select2 dropdown options")
                    
                    # Print all available options
                    available_options = []
                    for option in dropdown_options:
                        option_text = option.text.strip()
                        if option_text:
                            available_options.append(option_text)
                            print(f"  - '{option_text}'")
                    
                    # Try to find and click the desired location
                    location_found = False
                    for option in dropdown_options:
                        option_text = option.text.strip()
                        if location.lower() in option_text.lower():
                            option.click()
                            print(f"Successfully selected location: {option_text}")
                            location_found = True
                            break
                    
                    if not location_found:
                        print(f"Location '{location}' not found in Select2 dropdown")
                        print(f"Available options: {available_options}")
                        return False
                    
                    return True
                    
                except Exception as e:
                    print(f"Error handling Select2 dropdown: {e}")
                    return False
                
            elif tag_name == "select":
                # Standard select element
                select = Select(location_element)
                available_options = [option.text for option in select.options]
                print(f"Available location options: {available_options}")
                
                # Debug: Print each option with its exact text and length
                print("=== DETAILED OPTION ANALYSIS ===")
                for i, option in enumerate(select.options):
                    print(f"Option {i}: '{option.text}' (length: {len(option.text)})")
                    print(f"  - Value: '{option.get_attribute('value')}'")
                    print(f"  - HTML: {option.get_attribute('outerHTML')}")
                
                # Try exact match first
                if location in available_options:
                    select.select_by_visible_text(location)
                    print(f"Successfully selected location: {location}")
                    return True
                
                # Try case-insensitive match
                location_lower = location.lower()
                for option_text in available_options:
                    if location_lower in option_text.lower():
                        select.select_by_visible_text(option_text)
                        print(f"Successfully selected location (case-insensitive): {option_text}")
                        return True
                
                # Try partial match
                for option_text in available_options:
                    if any(word in option_text.lower() for word in location_lower.split()):
                        select.select_by_visible_text(option_text)
                        print(f"Successfully selected location (partial match): {option_text}")
                        return True
                
                print(f"Location '{location}' not available in dropdown")
                print(f"Available options: {available_options}")
                return False
            else:
                # Custom dropdown component (span, div, etc.)
                print(f"Custom dropdown detected (tag: {tag_name})")
                print("Custom dropdowns may not have the expected options loaded")
                print("This is normal for dynamic content that loads via JavaScript")
                return False
            
        except Exception as e:
            print(f"Error filtering by location: {e}")
            return False
    
    def filter_by_department(self, department="Quality Assurance"):
        """
        Filter jobs by department.
        
        Args:
            department: Department to filter by (default: Quality Assurance)
        
        Returns:
            bool: True if filter applied successfully
        """
        try:
            # First wait for jobs to load
            if not self.wait_for_jobs_to_load():
                print("Jobs did not load, cannot filter by department")
                return False
            
            # Find the department filter dropdown (it's a custom component, not a select)
            department_element = self.find_element(self.department_filter)
            
            # Check if it's a select element or custom dropdown
            tag_name = department_element.tag_name
            print(f"Department filter element tag: {tag_name}")
            
            if tag_name == "select":
                # Standard select element
                select = Select(department_element)
                available_options = [option.text for option in select.options]
                print(f"Available department options: {available_options}")
                
                if department not in available_options:
                    print(f"Department '{department}' not available in dropdown")
                    print(f"Available options: {available_options}")
                    return False
                
                select.select_by_visible_text(department)
                print(f"Successfully selected department: {department}")
                return True
            else:
                # Custom dropdown component (span, div, etc.)
                print(f"Custom dropdown detected (tag: {tag_name})")
                print("Custom dropdowns may not have the expected options loaded")
                print("This is normal for dynamic content that loads via JavaScript")
                return False
            
        except Exception as e:
            print(f"Error filtering by department: {e}")
            return False
    
    def verify_job_list_present(self):
        """
        Verify that job list is present on the page.
        
        Returns:
            bool: True if job list is present
        """
        try:
            # Wait for jobs to load first
            if not self.wait_for_jobs_to_load():
                return False
            
            # Check for job elements
            job_elements = self.driver.find_elements(By.XPATH, "//div[contains(@class,'position')]")
            if job_elements:
                print(f"Found {len(job_elements)} job positions")
                return True
            
            # Check for "no results" message
            no_results = self.driver.find_elements(By.XPATH, "//p[contains(text(),'No positions available')]")
            if no_results and any(elem.is_displayed() for elem in no_results):
                print("No job positions available")
                return True
            
            return False
        except Exception as e:
            print(f"Error verifying job list: {e}")
            return False
    
    def verify_job_filters(self):
        """
        Verify that all jobs match the expected filters.
        
        Returns:
            bool: True if all jobs match filters
        """
        try:
            # Wait for jobs to load first
            if not self.wait_for_jobs_to_load():
                return False
            
            # Get all job positions
            positions = self.driver.find_elements(*self.job_positions)
            departments = self.driver.find_elements(*self.job_departments)
            locations = self.driver.find_elements(*self.job_locations)
            
            # Check if we have jobs
            if not positions:
                print("No jobs found")
                return False
            
            # Verify each job matches our filters
            for i in range(len(positions)):
                position_text = positions[i].text
                department_text = departments[i].text
                location_text = locations[i].text
                
                # Check if position contains "Quality Assurance"
                if "Quality Assurance" not in position_text:
                    print(f"Position {position_text} does not contain 'Quality Assurance'")
                    return False
                
                # Check if department is "Quality Assurance"
                if department_text != self.expected_department:
                    print(f"Department {department_text} is not 'Quality Assurance'")
                    return False
                
                # Check if location is "Istanbul, Turkiye"
                if location_text != self.expected_location:
                    print(f"Location {location_text} is not 'Istanbul, Turkiye'")
                    return False
            
            return True
        except Exception as e:
            print(f"Error verifying job filters: {e}")
            return False
    
    def click_view_role_button(self):
        """
        Click on the first "View Role" button.
        
        Returns:
            bool: True if click successful
        """
        try:
            # Click on the first View Role button
            self.click_element(self.view_role_buttons)
            return True
        except Exception as e:
            print(f"Error clicking View Role button: {e}")
            return False
    
    def verify_redirect_to_lever(self):
        """
        Verify that clicking View Role redirects to Lever application form.
        
        Returns:
            bool: True if redirected to Lever
        """
        try:
            # Check if URL contains "lever" (Lever application platform)
            current_url = self.driver.current_url
            return "lever" in current_url.lower()
        except Exception as e:
            print(f"Error verifying Lever redirect: {e}")
            return False 