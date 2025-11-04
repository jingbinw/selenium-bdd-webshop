"""
Shopping cart page object
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ShoppingCartPage(BasePage):
    """Shopping cart page object class"""
    
    # Locators
    CART_ITEMS = (By.CSS_SELECTOR, ".cart-item-row")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".product-name")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".product-unit-price")
    QUANTITY_INPUTS = (By.CSS_SELECTOR, ".qty-input")
    SUBTOTALS = (By.CSS_SELECTOR, ".product-subtotal")
    
    # Cart actions
    UPDATE_CART_BUTTON = (By.CSS_SELECTOR, "input[name='updatecart']")
    REMOVE_CHECKBOXES = (By.CSS_SELECTOR, "input[name='removefromcart']")
    CONTINUE_SHOPPING_BUTTON = (By.CSS_SELECTOR, "input[value='Continue shopping']")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, "#checkout")
    
    # Cart totals
    CART_TOTAL = (By.CSS_SELECTOR, ".cart-total-right .value-summary")
    ORDER_TOTAL = (By.CSS_SELECTOR, ".product-price.order-total strong")
    
    # Empty cart
    EMPTY_CART_MESSAGE = (By.CSS_SELECTOR, ".order-summary-content")
    
    # Terms and conditions
    TERMS_CHECKBOX = (By.ID, "termsofservice")
    
    def navigate_to_cart(self):
        """Navigate to shopping cart page"""
        self.navigate_to("cart")
        self.wait_for_page_load()
    
    def get_cart_items_count(self):
        """Get number of items in cart"""
        items = self.driver.find_elements(*self.CART_ITEMS)
        return len(items)
    
    def get_product_names(self):
        """Get all product names in cart"""
        name_elements = self.driver.find_elements(*self.PRODUCT_NAMES)
        return [element.text for element in name_elements]
    
    def get_product_prices(self):
        """Get all product prices in cart"""
        price_elements = self.driver.find_elements(*self.PRODUCT_PRICES)
        return [element.text for element in price_elements]
    
    def get_product_quantities(self):
        """Get all product quantities in cart"""
        quantity_elements = self.driver.find_elements(*self.QUANTITY_INPUTS)
        return [int(element.get_attribute("value")) for element in quantity_elements]
    
    def update_quantity(self, item_index, new_quantity):
        """Update quantity for specific item"""
        quantity_inputs = self.driver.find_elements(*self.QUANTITY_INPUTS)
        if 0 <= item_index < len(quantity_inputs):
            quantity_input = quantity_inputs[item_index]
            quantity_input.clear()
            quantity_input.send_keys(str(new_quantity))
            return True
        return False
    
    def click_update_cart(self):
        """Click update cart button"""
        self.element_helper.click_element_safe(self.UPDATE_CART_BUTTON)
    
    def remove_item(self, item_index):
        """Remove item from cart by index"""
        remove_checkboxes = self.driver.find_elements(*self.REMOVE_CHECKBOXES)
        if 0 <= item_index < len(remove_checkboxes):
            remove_checkboxes[item_index].click()
            self.click_update_cart()
            return True
        return False
    
    def remove_all_items(self):
        """Remove all items from cart"""
        remove_checkboxes = self.driver.find_elements(*self.REMOVE_CHECKBOXES)
        for checkbox in remove_checkboxes:
            checkbox.click()
        
        if remove_checkboxes:
            self.click_update_cart()
            return True
        return False
    
    def get_cart_total(self):
        """Get cart total amount"""
        try:
            total_element = self.element_helper.find_element_safe(self.CART_TOTAL)
            return total_element.text if total_element else None
        except:
            return None
    
    def get_order_total(self):
        """Get order total amount"""
        try:
            total_element = self.element_helper.find_element_safe(self.ORDER_TOTAL)
            return total_element.text if total_element else None
        except:
            return None
    
    def click_continue_shopping(self):
        """Click continue shopping button"""
        # Wait for any notification messages to disappear
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
        
        # Now click continue shopping button
        self.element_helper.click_element_safe(self.CONTINUE_SHOPPING_BUTTON)
    
    def accept_terms_and_conditions(self):
        """Accept terms and conditions"""
        if self.is_element_displayed(self.TERMS_CHECKBOX):
            self.element_helper.click_element_safe(self.TERMS_CHECKBOX)
            return True
        return False
    
    def click_checkout(self):
        """Click checkout button"""
        self.element_helper.click_element_safe(self.CHECKOUT_BUTTON)
    
    def proceed_to_checkout(self):
        """Complete checkout process"""
        self.accept_terms_and_conditions()
        self.click_checkout()
    
    def is_cart_empty(self):
        """Check if cart is empty"""
        return self.get_cart_items_count() == 0
    
    def get_empty_cart_message(self):
        """Get empty cart message"""
        try:
            message_element = self.element_helper.find_element_safe(self.EMPTY_CART_MESSAGE)
            return message_element.text if message_element else None
        except:
            return None
    
    def has_items_in_cart(self):
        """Check if cart has items"""
        return self.get_cart_items_count() > 0
    
    def get_item_details(self, item_index):
        """Get details for specific cart item"""
        if item_index >= self.get_cart_items_count():
            return None
        
        names = self.get_product_names()
        prices = self.get_product_prices()
        quantities = self.get_product_quantities()
        
        return {
            'name': names[item_index] if item_index < len(names) else None,
            'price': prices[item_index] if item_index < len(prices) else None,
            'quantity': quantities[item_index] if item_index < len(quantities) else None
        }