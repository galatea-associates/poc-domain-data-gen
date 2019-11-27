import sys
import datetime

sys.path.insert(0, 'tests/')
from utils import shared_tests as shared
from utils import helper_methods as helper


def test_prices():
    records = helper.set_up_price_tests()
    for record in records:
        shared.attribute_quantity_valid('price', record, 5)
        shared.price_valid(record)
        shared.currency_valid(record)
        correct_datetime(record['created_timestamp'])
        correct_datetime(record['last_updated_time_stamp'])


def correct_datetime(price_datetime):
    """Ensure that the datetime passed in has a date value that matches the
     current date in UTC"""
    assert price_datetime.date() == datetime.datetime.now(
        datetime.timezone.utc).date()
