"""
WebDriver factory and manager
"""
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from config import config


class WebDriverFactory:
    """Factory class for creating WebDriver instances"""
    
    @staticmethod
    def create_driver(browser_name=None, headless=None):
        """
        Create and return a WebDriver instance
        
        Args:
            browser_name (str): Browser name (chrome, firefox, edge)
            headless (bool): Whether to run in headless mode
            
        Returns:
            WebDriver: Configured WebDriver instance
        """
        browser = browser_name or config.browser
        is_headless = headless if headless is not None else config.headless
        
        if browser.lower() == 'chrome':
            return WebDriverFactory._create_chrome_driver(is_headless)
        elif browser.lower() == 'firefox':
            return WebDriverFactory._create_firefox_driver(is_headless)
        elif browser.lower() == 'edge':
            return WebDriverFactory._create_edge_driver(is_headless)
        else:
            raise ValueError(f"Unsupported browser: {browser}")
    
    @staticmethod
    def _create_chrome_driver(headless):
        """Create Chrome WebDriver"""
        options = ChromeOptions()
        
        if headless:
            options.add_argument('--headless')
        
        # Essential options for CI and stability
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        # Anti-detection options
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Let webdriver-manager handle ChromeDriver installation and path resolution
        chrome_driver_path = ChromeDriverManager().install()
        
        # Simple fix for macOS path issue
        if chrome_driver_path.endswith('THIRD_PARTY_NOTICES.chromedriver'):
            chrome_driver_path = chrome_driver_path.replace('THIRD_PARTY_NOTICES.chromedriver', 'chromedriver')
        
        service = ChromeService(chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    
    @staticmethod
    def _create_firefox_driver(headless):
        """Create Firefox WebDriver"""
        options = FirefoxOptions()
        
        if headless:
            options.add_argument('--headless')
        
        options.add_argument('--width=1920')
        options.add_argument('--height=1080')
        
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)
    
    @staticmethod
    def _create_edge_driver(headless):
        """Create Edge WebDriver"""
        options = EdgeOptions()
        
        if headless:
            options.add_argument('--headless')
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=options)


class WebDriverManager:
    """Singleton WebDriver manager"""
    
    _instance = None
    _driver = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_driver(self, browser_name=None, headless=None):
        """Get or create WebDriver instance"""
        if self._driver is None:
            self._driver = WebDriverFactory.create_driver(browser_name, headless)
            self._configure_driver()
        return self._driver
    
    def quit_driver(self):
        """Quit the WebDriver instance"""
        if self._driver:
            self._driver.quit()
            self._driver = None
    
    def _configure_driver(self):
        """Configure WebDriver with timeouts"""
        if self._driver:
            self._driver.implicitly_wait(config.implicit_wait)
            self._driver.set_page_load_timeout(config.page_load_timeout)
            self._driver.maximize_window()