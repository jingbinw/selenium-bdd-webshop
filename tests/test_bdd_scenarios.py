"""
Test runner for BDD scenarios
"""
import pytest
from pytest_bdd import scenarios

# Import step definitions so they are registered
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from features.steps.login_steps import *
from features.steps.shopping_steps import *

# Load all scenarios from feature files
scenarios('../features/login.feature')
scenarios('../features/shopping_cart.feature') 
scenarios('../features/end_to_end.feature')