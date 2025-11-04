"""
Simple configuration using environment variables
"""
import os
from pathlib import Path


def load_env_file():
    """Load environment variables from .env file"""
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()


class Config:
    """Simple configuration class using environment variables with defaults"""
    
    def __init__(self):
        # Load environment variables from .env file first
        load_env_file()
    
    @property
    def base_url(self):
        return os.getenv('BASE_URL', 'https://demowebshop.tricentis.com/')
    
    @property
    def browser(self):
        return os.getenv('BROWSER', 'chrome')
    
    @property
    def headless(self):
        return os.getenv('HEADLESS', 'false').lower() == 'true'
    
    @property
    def implicit_wait(self):
        return int(os.getenv('IMPLICIT_WAIT', '10'))
    
    @property
    def explicit_wait(self):
        return int(os.getenv('EXPLICIT_WAIT', '20'))
    
    @property
    def page_load_timeout(self):
        return int(os.getenv('PAGE_LOAD_TIMEOUT', '30'))
    
    @property
    def test_email(self):
        return os.getenv('TEST_EMAIL', '')
    
    @property
    def test_password(self):
        return os.getenv('TEST_PASSWORD', '')
    
    @property
    def screenshot_on_failure(self):
        return os.getenv('SCREENSHOT_ON_FAILURE', 'true').lower() == 'true'
    
    @property
    def environment(self):
        return os.getenv('ENVIRONMENT', 'test')


# Global config instance
config = Config()