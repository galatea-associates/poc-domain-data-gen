import sys
sys.path.insert(0, 'tests/')
from utils import shared_tests as shared
from utils import helper_methods as helper


def test_prices():
    records = helper.set_up_price_tests()
    for record in records:
        shared.attribute_quantity_valid(record, 4)
        shared.ric_exists(record)
        shared.price_valid(record)
        shared.currency_valid(record)
