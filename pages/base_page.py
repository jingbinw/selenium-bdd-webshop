"""
Base page class for all page objects
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from utils.helpers import WaitHelper, ElementHelper, ScreenshotHelper
from config import config


class BasePage:
    """Base page class with common functionality"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait_helper = WaitHelper(driver)
        self.element_helper = ElementHelper(driver)
        self.base_url = config.base_url
    
    def navigate_to(self, url):
        """Navigate to a specific URL"""
        full_url = f"{self.base_url.rstrip('/')}/{url.lstrip('/')}" if not url.startswith('http') else url
        self.driver.get(full_url)
    
    def get_current_url(self):
        """Get current page URL"""
        return self.driver.current_url
    
    def get_page_title(self):
        """Get page title"""
        return self.driver.title
    
    def take_screenshot(self, name=None):
        """Take a screenshot of the current page"""
        return ScreenshotHelper.take_screenshot(self.driver, name)
    
    def refresh_page(self):
        """Refresh the current page"""
        self.driver.refresh()
    
    def scroll_to_top(self):
        """Scroll to top of the page"""
        self.driver.execute_script("window.scrollTo(0, 0);")
    
    def scroll_to_bottom(self):
        """Scroll to bottom of the page"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    def wait_for_page_load(self):
        """Wait for page to load completely"""
        self.wait_helper.wait_for_element_present((By.TAG_NAME, "body"))
    
    def select_dropdown_by_text(self, locator, text):
        """Select dropdown option by visible text"""
        element = self.wait_helper.wait_for_element_visible(locator)
        select = Select(element)
        select.select_by_visible_text(text)
    
    def select_dropdown_by_value(self, locator, value):
        """Select dropdown option by value"""
        element = self.wait_helper.wait_for_element_visible(locator)
        select = Select(element)
        select.select_by_value(value)
    
    def get_element_attribute(self, locator, attribute):
        """Get element attribute value"""
        element = self.wait_helper.wait_for_element_visible(locator)
        return element.get_attribute(attribute)
    
    def is_element_displayed(self, locator):
        """Check if element is displayed"""
        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except:
            return False