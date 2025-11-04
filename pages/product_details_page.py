"""
Product details page object
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductDetailsPage(BasePage):
    """Product details page object class"""
    
    # Locators
    PRODUCT_NAME = (By.CSS_SELECTOR, ".product-name h1")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".price-value-27")
    PRODUCT_SKU = (By.CSS_SELECTOR, ".sku .value")
    PRODUCT_DESCRIPTION = (By.CSS_SELECTOR, ".full-description")
    PRODUCT_IMAGE = (By.CSS_SELECTOR, ".picture img")
    
    # Add to cart section
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, ".add-to-cart-button")
    QUANTITY_INPUT = (By.CSS_SELECTOR, ".qty-input")
    
    # Success message
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".bar-notification.success")
    CLOSE_NOTIFICATION = (By.CSS_SELECTOR, ".close")
    
    # Product attributes (may vary by product)
    PRODUCT_ATTRIBUTES = (By.CSS_SELECTOR, ".product-attributes")
    
    # Reviews section
    REVIEWS_SECTION = (By.CSS_SELECTOR, ".product-review-box")
    REVIEW_BUTTON = (By.CSS_SELECTOR, ".write-product-review-button")
    
    def get_product_name(self):
        """Get product name"""
        return self.element_helper.get_text_safe(self.PRODUCT_NAME)
    
    def get_product_price(self):
        """Get product price"""
        return self.element_helper.get_text_safe(self.PRODUCT_PRICE)
    
    def get_product_sku(self):
        """Get product SKU"""
        try:
            return self.element_helper.get_text_safe(self.PRODUCT_SKU)
        except:
            return None
    
    def get_product_description(self):
        """Get product description"""
        try:
            return self.element_helper.get_text_safe(self.PRODUCT_DESCRIPTION)
        except:
            return None
    
    def set_quantity(self, quantity):
        """Set product quantity"""
        quantity_field = self.element_helper.find_element_safe(self.QUANTITY_INPUT)
        if quantity_field:
            quantity_field.clear()
            quantity_field.send_keys(str(quantity))
    
    def get_quantity(self):
        """Get current quantity value"""
        quantity_field = self.element_helper.find_element_safe(self.QUANTITY_INPUT)
        if quantity_field:
            return int(quantity_field.get_attribute("value"))
        return 1
    
    def click_add_to_cart(self):
        """Click add to cart button"""
        self.element_helper.click_element_safe(self.ADD_TO_CART_BUTTON)
    
    def add_to_cart_with_quantity(self, quantity=1):
        """Add product to cart with specified quantity"""
        if quantity > 1:
            self.set_quantity(quantity)
        self.click_add_to_cart()
    
    def get_success_message(self):
        """Get success message after adding to cart"""
        try:
            success_element = self.wait_helper.wait_for_element_visible(self.SUCCESS_MESSAGE)
            return success_element.text
        except:
            return None
    
    def close_success_notification(self):
        """Close success notification"""
        try:
            self.element_helper.click_element_safe(self.CLOSE_NOTIFICATION)
        except:
            pass  # Notification might auto-close
    
    def is_add_to_cart_button_enabled(self):
        """Check if add to cart button is enabled"""
        button = self.element_helper.find_element_safe(self.ADD_TO_CART_BUTTON)
        if button:
            return button.is_enabled()
        return False
    
    def get_product_image_src(self):
        """Get product image source URL"""
        image = self.element_helper.find_element_safe(self.PRODUCT_IMAGE)
        if image:
            return image.get_attribute("src")
        return None
    
    def click_product_image(self):
        """Click on product image"""
        self.element_helper.click_element_safe(self.PRODUCT_IMAGE)
    
    def has_reviews_section(self):
        """Check if product has reviews section"""
        return self.is_element_displayed(self.REVIEWS_SECTION)
    
    def click_write_review(self):
        """Click write review button"""
        if self.is_element_displayed(self.REVIEW_BUTTON):
            self.element_helper.click_element_safe(self.REVIEW_BUTTON)
            return True
        return False