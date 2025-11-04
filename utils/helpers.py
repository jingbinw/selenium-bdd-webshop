"""
Common utilities for test framework
"""
import os
import time
from datetime import datetime
from pathlib import Path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config import config


class WaitHelper:
    """Helper class for explicit waits"""
    
    def __init__(self, driver, timeout=None):
        self.driver = driver
        self.timeout = timeout or config.explicit_wait
        self.wait = WebDriverWait(driver, self.timeout)
    
    def wait_for_element_visible(self, locator):
        """Wait for element to be visible"""
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not visible after {self.timeout} seconds")
    
    def wait_for_element_clickable(self, locator):
        """Wait for element to be clickable"""
        try:
            return self.wait.until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not clickable after {self.timeout} seconds")
    
    def wait_for_element_present(self, locator):
        """Wait for element to be present in DOM"""
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not present after {self.timeout} seconds")
    
    def wait_for_text_in_element(self, locator, text):
        """Wait for specific text in element"""
        try:
            return self.wait.until(EC.text_to_be_present_in_element(locator, text))
        except TimeoutException:
            raise TimeoutException(f"Text '{text}' not found in element {locator} after {self.timeout} seconds")
    
    def wait_for_url_contains(self, url_part):
        """Wait for URL to contain specific text"""
        try:
            return self.wait.until(EC.url_contains(url_part))
        except TimeoutException:
            raise TimeoutException(f"URL does not contain '{url_part}' after {self.timeout} seconds")


class ScreenshotHelper:
    """Helper class for taking screenshots"""
    
    @staticmethod
    def take_screenshot(driver, test_name=None):
        """Take a screenshot and save it"""
        if not config.screenshot_on_failure:
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = test_name or "screenshot"
        filename = f"{test_name}_{timestamp}.png"
        
        # Create screenshots directory
        screenshots_dir = Path("reports/screenshots")
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        
        screenshot_path = screenshots_dir / filename
        
        try:
            driver.save_screenshot(str(screenshot_path))
            return str(screenshot_path)
        except Exception as e:
            print(f"Failed to take screenshot: {e}")
            return None


class TestDataHelper:
    """Helper class for test data management"""
    
    @staticmethod
    def generate_unique_email():
        """Generate a unique email for testing"""
        timestamp = int(time.time())
        return f"testuser_{timestamp}@example.com"
    
    @staticmethod
    def get_test_credentials():
        """Get test credentials"""
        return {
            'email': config.test_email,
            'password': config.test_password
        }


class ElementHelper:
    """Helper class for common element operations"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait_helper = WaitHelper(driver)
    
    def find_element_safe(self, locator):
        """Find element safely with explicit wait"""
        try:
            return self.wait_helper.wait_for_element_visible(locator)
        except TimeoutException:
            return None
    
    def click_element_safe(self, locator):
        """Click element safely with explicit wait"""
        element = self.wait_helper.wait_for_element_clickable(locator)
        element.click()
        return element
    
    def send_keys_safe(self, locator, text):
        """Send keys to element safely"""
        element = self.wait_helper.wait_for_element_visible(locator)
        element.clear()
        element.send_keys(text)
        return element
    
    def get_text_safe(self, locator):
        """Get text from element safely"""
        element = self.wait_helper.wait_for_element_visible(locator)
        return element.text
    
    def is_element_present(self, locator):
        """Check if element is present"""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def scroll_to_element(self, locator):
        """Scroll to element"""
        element = self.wait_helper.wait_for_element_present(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        return element