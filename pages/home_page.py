"""
Home page object
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomePage(BasePage):
    """Home page object class"""
    
    # Locators
    SEARCH_BOX = (By.ID, "small-searchterms")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "input[value='Search']")
    LOGIN_LINK = (By.LINK_TEXT, "Log in")
    REGISTER_LINK = (By.LINK_TEXT, "Register")
    LOGOUT_LINK = (By.LINK_TEXT, "Log out")
    MY_ACCOUNT_LINK = (By.LINK_TEXT, "My account")
    SHOPPING_CART_LINK = (By.ID, "topcartlink")
    CART_QUANTITY = (By.CSS_SELECTOR, ".cart-qty")
    
    # Category links
    BOOKS_CATEGORY = (By.XPATH, "//a[contains(@href, '/books')]")
    COMPUTERS_CATEGORY = (By.XPATH, "//a[contains(@href, '/computers')]")
    ELECTRONICS_CATEGORY = (By.XPATH, "//a[contains(@href, '/electronics')]")
    
    # Navigation menu
    NAVIGATION_MENU = (By.CSS_SELECTOR, ".header-menu")
    
    def navigate_to_home(self):
        """Navigate to home page"""
        self.navigate_to("")
        self.wait_for_page_load()
    
    def search_product(self, search_term):
        """Search for a product"""
        self.element_helper.send_keys_safe(self.SEARCH_BOX, search_term)
        self.element_helper.click_element_safe(self.SEARCH_BUTTON)
    
    def click_login_link(self):
        """Click on login link"""
        self.element_helper.click_element_safe(self.LOGIN_LINK)
    
    def click_register_link(self):
        """Click on register link"""
        self.element_helper.click_element_safe(self.REGISTER_LINK)
    
    def click_logout_link(self):
        """Click on logout link"""
        self.element_helper.click_element_safe(self.LOGOUT_LINK)
    
    def click_my_account_link(self):
        """Click on my account link"""
        self.element_helper.click_element_safe(self.MY_ACCOUNT_LINK)
    
    def click_shopping_cart(self):
        """Click on shopping cart link"""
        # Wait for any notification messages to disappear before clicking cart
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        from selenium.common.exceptions import TimeoutException
        
        try:
            # Wait for notification to disappear (if present)
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, '#bar-notification'))
            )
        except TimeoutException:
            pass  # If no notification found, continue
        
        self.element_helper.click_element_safe(self.SHOPPING_CART_LINK)
    
    def get_cart_quantity(self):
        """Get the quantity of items in cart"""
        try:
            cart_qty_element = self.element_helper.find_element_safe(self.CART_QUANTITY)
            if cart_qty_element:
                qty_text = cart_qty_element.text.strip('()')
                return int(qty_text) if qty_text.isdigit() else 0
            return 0
        except:
            return 0
    
    def click_books_category(self):
        """Click on books category"""
        self.element_helper.click_element_safe(self.BOOKS_CATEGORY)
    
    def click_computers_category(self):
        """Click on computers category"""
        self.element_helper.click_element_safe(self.COMPUTERS_CATEGORY)
    
    def click_electronics_category(self):
        """Click on electronics category"""
        self.element_helper.click_element_safe(self.ELECTRONICS_CATEGORY)
    
    def is_logged_in(self):
        """Check if user is logged in"""
        return self.is_element_displayed(self.LOGOUT_LINK)
    
    def is_logged_out(self):
        """Check if user is logged out"""
        return self.is_element_displayed(self.LOGIN_LINK)
    
    def get_search_box_placeholder(self):
        """Get search box placeholder text"""
        return self.get_element_attribute(self.SEARCH_BOX, "placeholder")