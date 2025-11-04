"""
Pytest configuration and fixtures
"""
import pytest
import allure
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
from utils import WebDriverManager, ScreenshotHelper
from config import config


class TestEventListener(AbstractEventListener):
    """Event listener for WebDriver events"""
    
    def on_exception(self, exception, driver):
        """Handle exceptions during test execution"""
        test_name = pytest.current_pytest_item.name if hasattr(pytest, 'current_pytest_item') else 'exception'
        ScreenshotHelper.take_screenshot(driver, f"exception_{test_name}")


@pytest.fixture(scope='session')
def driver_manager():
    """Session-scoped driver manager"""
    return WebDriverManager()


@pytest.fixture(scope='function') 
def driver(driver_manager):
    """Function-scoped WebDriver instance"""
    driver_instance = driver_manager.get_driver()
    
    # Add event listener for better debugging
    event_driver = EventFiringWebDriver(driver_instance, TestEventListener())
    
    yield event_driver
    
    # Cleanup
    driver_manager.quit_driver()


@pytest.fixture(scope='function')
def browser_context(driver_manager):
    """Browser context fixture for BDD tests"""
    driver = driver_manager.get_driver()
    
    context = {
        'driver': driver,
        'driver_manager': driver_manager,
        'base_url': config.base_url
    }
    
    yield context
    
    # Cleanup after test
    if hasattr(context.get('driver'), 'quit'):
        context['driver_manager'].quit_driver()


@pytest.fixture(autouse=True)
def allure_environment():
    """Set up Allure environment information"""
    try:
        # Only set environment if allure is properly configured
        if hasattr(allure, 'environment'):
            allure.environment(
                browser=config.browser,
                base_url=config.base_url,
                environment=config.environment
            )
    except Exception:
        # Silently ignore allure configuration issues
        pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results and add screenshots to Allure"""
    outcome = yield
    rep = outcome.get_result()
    
    # Store the report in the item for later use
    setattr(item, f"rep_{rep.when}", rep)
    
    # Add screenshot to Allure on failure
    if rep.when == "call" and rep.failed:
        if hasattr(item, 'funcargs') and 'driver' in item.funcargs:
            driver = item.funcargs['driver']
            screenshot_path = ScreenshotHelper.take_screenshot(driver, item.name)
            
            if screenshot_path:
                with open(screenshot_path, 'rb') as f:
                    allure.attach(
                        f.read(),
                        name=f"Screenshot_{item.name}",
                        attachment_type=allure.attachment_type.PNG
                    )
        # Also handle browser_context fixture for BDD tests
        elif hasattr(item, 'funcargs') and 'browser_context' in item.funcargs:
            browser_context = item.funcargs['browser_context']
            screenshot_path = ScreenshotHelper.take_screenshot(browser_context['driver'], item.name)
            
            if screenshot_path:
                with open(screenshot_path, 'rb') as f:
                    allure.attach(
                        f.read(),
                        name=f"Screenshot_{item.name}",
                        attachment_type=allure.attachment_type.PNG
                    )


@pytest.fixture(autouse=True)
def setup_test_data(request):
    """Setup test data and metadata"""
    # Set current test item for event listener
    pytest.current_pytest_item = request.node
    
    # Add test metadata to Allure
    if hasattr(request.node, 'get_closest_marker'):
        smoke_marker = request.node.get_closest_marker('smoke')
        if smoke_marker:
            allure.dynamic.tag("smoke")
            
        regression_marker = request.node.get_closest_marker('regression')
        if regression_marker:
            allure.dynamic.tag("regression")
            
        login_marker = request.node.get_closest_marker('login')
        if login_marker:
            allure.dynamic.feature("Login")
            
        shopping_marker = request.node.get_closest_marker('shopping')
        if shopping_marker:
            allure.dynamic.feature("Shopping Cart")
            
        e2e_marker = request.node.get_closest_marker('e2e')
        if e2e_marker:
            allure.dynamic.feature("End-to-End")


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )
    config.addinivalue_line(
        "markers", "login: mark test as login related"
    )
    config.addinivalue_line(
        "markers", "shopping: mark test as shopping cart related"
    )
    config.addinivalue_line(
        "markers", "e2e: mark test as end-to-end"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )