"""
Search results page object
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class SearchResultsPage(BasePage):
    """Search results page object class"""
    
    # Locators
    SEARCH_RESULTS = (By.CSS_SELECTOR, ".search-results")
    PRODUCT_ITEMS = (By.CSS_SELECTOR, ".product-item")
    PRODUCT_TITLES = (By.CSS_SELECTOR, ".product-title a")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".price")
    PRODUCT_IMAGES = (By.CSS_SELECTOR, ".picture img")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "input[value='Add to cart']")
    
    # Search info
    SEARCH_TERM_DISPLAY = (By.CSS_SELECTOR, ".search-term")
    RESULTS_COUNT = (By.CSS_SELECTOR, ".product-selectors")
    NO_RESULTS_MESSAGE = (By.CSS_SELECTOR, ".no-result")
    
    # Sorting and filtering
    SORT_DROPDOWN = (By.ID, "products-orderby")
    PAGE_SIZE_DROPDOWN = (By.ID, "products-pagesize")
    VIEW_MODE_LIST = (By.CSS_SELECTOR, ".list-view")
    VIEW_MODE_GRID = (By.CSS_SELECTOR, ".grid-view")
    
    # Pagination
    PAGINATION = (By.CSS_SELECTOR, ".pager")
    NEXT_PAGE = (By.CSS_SELECTOR, ".next-page")
    PREVIOUS_PAGE = (By.CSS_SELECTOR, ".previous-page")
    PAGE_NUMBERS = (By.CSS_SELECTOR, ".individual-page")
    
    def has_search_results(self):
        """Check if search results are displayed"""
        try:
            return (self.is_element_displayed(self.SEARCH_RESULTS) and 
                    self.get_search_results_count() > 0)
        except:
            return False
    
    def get_search_results_count(self):
        """Get number of search results"""
        try:
            product_items = self.driver.find_elements(*self.PRODUCT_ITEMS)
            return len(product_items)
        except:
            return 0
    
    def get_product_titles(self):
        """Get all product titles from search results"""
        try:
            title_elements = self.driver.find_elements(*self.PRODUCT_TITLES)
            return [element.text for element in title_elements]
        except:
            return []
    
    def get_product_prices(self):
        """Get all product prices from search results"""
        try:
            price_elements = self.driver.find_elements(*self.PRODUCT_PRICES)
            return [element.text for element in price_elements]
        except:
            return []
    
    def click_product_by_index(self, index):
        """Click on product by index"""
        try:
            product_titles = self.driver.find_elements(*self.PRODUCT_TITLES)
            if 0 <= index < len(product_titles):
                product_titles[index].click()
                return True
            return False
        except:
            return False
    
    def click_product_by_title(self, title):
        """Click on product by title"""
        try:
            product_titles = self.driver.find_elements(*self.PRODUCT_TITLES)
            for product in product_titles:
                if title.lower() in product.text.lower():
                    product.click()
                    return True
            return False
        except:
            return False
    
    def add_product_to_cart_by_index(self, index):
        """Add product to cart by index"""
        try:
            add_to_cart_buttons = self.driver.find_elements(*self.ADD_TO_CART_BUTTONS)
            if 0 <= index < len(add_to_cart_buttons):
                add_to_cart_buttons[index].click()
                return True
            return False
        except:
            return False
    
    def get_displayed_search_term(self):
        """Get the search term displayed on the page"""
        try:
            search_term_element = self.element_helper.find_element_safe(self.SEARCH_TERM_DISPLAY)
            return search_term_element.text if search_term_element else None
        except:
            return None
    
    def has_no_results_message(self):
        """Check if no results message is displayed"""
        return self.is_element_displayed(self.NO_RESULTS_MESSAGE)
    
    def get_no_results_message(self):
        """Get no results message text"""
        try:
            message_element = self.element_helper.find_element_safe(self.NO_RESULTS_MESSAGE)
            return message_element.text if message_element else None
        except:
            return None
    
    def sort_by_option(self, option_text):
        """Sort results by option"""
        try:
            self.select_dropdown_by_text(self.SORT_DROPDOWN, option_text)
            return True
        except:
            return False
    
    def change_page_size(self, size):
        """Change number of items per page"""
        try:
            self.select_dropdown_by_text(self.PAGE_SIZE_DROPDOWN, str(size))
            return True
        except:
            return False
    
    def switch_to_list_view(self):
        """Switch to list view"""
        try:
            self.element_helper.click_element_safe(self.VIEW_MODE_LIST)
            return True
        except:
            return False
    
    def switch_to_grid_view(self):
        """Switch to grid view"""
        try:
            self.element_helper.click_element_safe(self.VIEW_MODE_GRID)
            return True
        except:
            return False
    
    def has_pagination(self):
        """Check if pagination is present"""
        return self.is_element_displayed(self.PAGINATION)
    
    def click_next_page(self):
        """Click next page in pagination"""
        try:
            if self.is_element_displayed(self.NEXT_PAGE):
                self.element_helper.click_element_safe(self.NEXT_PAGE)
                return True
            return False
        except:
            return False
    
    def click_previous_page(self):
        """Click previous page in pagination"""
        try:
            if self.is_element_displayed(self.PREVIOUS_PAGE):
                self.element_helper.click_element_safe(self.PREVIOUS_PAGE)
                return True
            return False
        except:
            return False
    
    def click_page_number(self, page_number):
        """Click specific page number"""
        try:
            page_elements = self.driver.find_elements(*self.PAGE_NUMBERS)
            for page_element in page_elements:
                if page_element.text == str(page_number):
                    page_element.click()
                    return True
            return False
        except:
            return False
    
    def get_product_details_by_index(self, index):
        """Get product details by index"""
        try:
            titles = self.get_product_titles()
            prices = self.get_product_prices()
            
            if 0 <= index < len(titles):
                return {
                    'title': titles[index] if index < len(titles) else None,
                    'price': prices[index] if index < len(prices) else None
                }
            return None
        except:
            return None