"""
Common step definitions for BDD tests
"""
import pytest
from pytest_bdd import given, when, then, parsers
from pages import HomePage, LoginPage, SearchResultsPage, ProductDetailsPage, ShoppingCartPage
from utils import WebDriverManager, TestDataHelper
from config import config


@given('I am on the demo webshop homepage')
def navigate_to_homepage(browser_context):
    """Navigate to the demo webshop homepage"""
    home_page = HomePage(browser_context['driver'])
    home_page.navigate_to_home()
    browser_context['home_page'] = home_page


@when('I click on the login link')
def click_login_link(browser_context):
    """Click on the login link"""
    home_page = browser_context['home_page']
    home_page.click_login_link()


@then('I should be on the login page')
def verify_login_page(browser_context):
    """Verify that we are on the login page"""
    login_page = LoginPage(browser_context['driver'])
    browser_context['login_page'] = login_page
    assert login_page.is_login_form_displayed(), "Login form is not displayed"


@when('I enter valid login credentials')
def enter_valid_credentials(browser_context):
    """Enter valid login credentials"""
    # Create login_page if it doesn't exist
    if 'login_page' not in browser_context:
        login_page = LoginPage(browser_context['driver'])
        browser_context['login_page'] = login_page
    else:
        login_page = browser_context['login_page']
    
    test_data = TestDataHelper.get_test_credentials()
    login_page.enter_email(test_data['email'])
    login_page.enter_password(test_data['password'])


@when('I click the login button')
def click_login_button(browser_context):
    """Click the login button"""
    login_page = browser_context['login_page']
    login_page.click_login_button()


@then('I should be logged in successfully')
def verify_successful_login(browser_context):
    """Verify successful login"""
    home_page = HomePage(browser_context['driver'])
    browser_context['home_page'] = home_page
    assert home_page.is_logged_in(), "User is not logged in"


@then('I should see the logout link')
def verify_logout_link(browser_context):
    """Verify logout link is visible"""
    home_page = browser_context['home_page']
    assert home_page.is_logged_in(), "Logout link is not visible"


@when(parsers.parse('I enter an invalid email "{email}"'))
def enter_invalid_email(browser_context, email):
    """Enter invalid email"""
    login_page = browser_context['login_page']
    login_page.enter_email(email)


@when('I enter a valid password')
def enter_valid_password(browser_context):
    """Enter valid password"""
    login_page = browser_context['login_page']
    test_data = TestDataHelper.get_test_credentials()
    login_page.enter_password(test_data['password'])


@when('I enter a valid email')
def enter_valid_email(browser_context):
    """Enter valid email"""
    login_page = browser_context['login_page']
    test_data = TestDataHelper.get_test_credentials()
    login_page.enter_email(test_data['email'])


@when(parsers.parse('I enter an invalid password "{password}"'))
def enter_invalid_password(browser_context, password):
    """Enter invalid password"""
    login_page = browser_context['login_page']
    login_page.enter_password(password)


@when('I leave the email field empty')
def leave_email_empty(browser_context):
    """Leave email field empty"""
    login_page = browser_context['login_page']
    login_page.enter_email("")


@when('I leave the password field empty')
def leave_password_empty(browser_context):
    """Leave password field empty"""
    login_page = browser_context['login_page']
    login_page.enter_password("")


@then('I should see an error message')
def verify_error_message(browser_context):
    """Verify error message is displayed"""
    login_page = browser_context['login_page']
    error_message = login_page.get_error_message()
    assert error_message is not None, "No error message is displayed"


@then('I should see validation error messages')
def verify_validation_errors(browser_context):
    """Verify validation error messages"""
    login_page = browser_context['login_page']
    error_message = login_page.get_error_message()
    assert error_message is not None, "No validation errors are displayed"


@then('I should see an authentication error message')
def verify_auth_error(browser_context):
    """Verify authentication error message"""
    login_page = browser_context['login_page']
    error_message = login_page.get_error_message()
    assert error_message is not None, "No authentication error is displayed"


@then('I should remain on the login page')
def verify_still_on_login_page(browser_context):
    """Verify still on login page"""
    login_page = browser_context['login_page']
    assert login_page.is_login_form_displayed(), "Not on login page"


@when('I click on the register link')
def click_register_link(browser_context):
    """Click on register link"""
    login_page = browser_context['login_page']
    login_page.click_register_link()


@then('I should be redirected to the registration page')
def verify_registration_page(browser_context):
    """Verify redirection to registration page"""
    driver = browser_context['driver']
    assert "register" in driver.current_url.lower(), "Not redirected to registration page"