"""
Pages package initialization
"""
from .base_page import BasePage
from .home_page import HomePage
from .login_page import LoginPage
from .search_results_page import SearchResultsPage
from .product_details_page import ProductDetailsPage
from .shopping_cart_page import ShoppingCartPage

__all__ = [
    'BasePage',
    'HomePage',
    'LoginPage', 
    'SearchResultsPage',
    'ProductDetailsPage',
    'ShoppingCartPage'
]