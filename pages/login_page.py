"""
Login page object
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Login page object class"""
    
    # Locators
    EMAIL_INPUT = (By.ID, "Email")
    PASSWORD_INPUT = (By.ID, "Password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "input[value='Log in']")
    REMEMBER_ME_CHECKBOX = (By.ID, "RememberMe")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot password?")
    REGISTER_LINK = (By.LINK_TEXT, "Register")
    
    # Error messages
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".message-error")
    VALIDATION_SUMMARY = (By.CSS_SELECTOR, ".validation-summary-errors")
    
    # Success indicators
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".message-success")
    
    def navigate_to_login(self):
        """Navigate to login page"""
        self.navigate_to("login")
        self.wait_for_page_load()
    
    def enter_email(self, email):
        """Enter email address"""
        self.element_helper.send_keys_safe(self.EMAIL_INPUT, email)
    
    def enter_password(self, password):
        """Enter password"""
        self.element_helper.send_keys_safe(self.PASSWORD_INPUT, password)
    
    def click_login_button(self):
        """Click login button"""
        self.element_helper.click_element_safe(self.LOGIN_BUTTON)
    
    def click_remember_me(self):
        """Click remember me checkbox"""
        self.element_helper.click_element_safe(self.REMEMBER_ME_CHECKBOX)
    
    def click_forgot_password(self):
        """Click forgot password link"""
        self.element_helper.click_element_safe(self.FORGOT_PASSWORD_LINK)
    
    def click_register_link(self):
        """Click register link"""
        self.element_helper.click_element_safe(self.REGISTER_LINK)
    
    def login(self, email, password, remember_me=False):
        """Perform complete login process"""
        self.enter_email(email)
        self.enter_password(password)
        
        if remember_me:
            self.click_remember_me()
        
        self.click_login_button()
    
    def get_error_message(self):
        """Get error message text"""
        try:
            error_element = self.element_helper.find_element_safe(self.ERROR_MESSAGE)
            if error_element:
                return error_element.text
            
            # Check validation summary for errors
            validation_element = self.element_helper.find_element_safe(self.VALIDATION_SUMMARY)
            if validation_element:
                return validation_element.text
            
            return None
        except:
            return None
    
    def get_success_message(self):
        """Get success message text"""
        try:
            success_element = self.element_helper.find_element_safe(self.SUCCESS_MESSAGE)
            return success_element.text if success_element else None
        except:
            return None
    
    def is_login_form_displayed(self):
        """Check if login form is displayed"""
        return (self.is_element_displayed(self.EMAIL_INPUT) and 
                self.is_element_displayed(self.PASSWORD_INPUT) and 
                self.is_element_displayed(self.LOGIN_BUTTON))
    
    def clear_form(self):
        """Clear login form fields"""
        email_field = self.element_helper.find_element_safe(self.EMAIL_INPUT)
        password_field = self.element_helper.find_element_safe(self.PASSWORD_INPUT)
        
        if email_field:
            email_field.clear()
        if password_field:
            password_field.clear()