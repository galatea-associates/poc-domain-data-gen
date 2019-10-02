import sys
sys.path.insert(0, 'tests/')
import pytest
from test_domain_objects import shared_tests as shared
from test_domain_objects import helper_methods as helper

def test_prices():
    records = helper.set_up_price_tests()
    for record in records:
        shared.ric_exists(record)
        shared.price_valid(record)
        shared.currency_valid(record)