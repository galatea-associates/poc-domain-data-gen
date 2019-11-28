import sys

sys.path.insert(0, 'tests/')
from utils import shared_tests as shared
from utils import helper_methods as helper


def test_trades():
    records = helper.set_up_trade_tests()
    shared.unique_ids(records, 'trade')
    for record in records:
        shared.attribute_quantity_valid('trade', record, 18)
        contract_id_valid(record)
        booking_datetime_valid(record)
        trade_datetime_valid(record)
        value_datetime_valid(record)
        order_id_valid(record)
        account_id_valid(record)
        counterparty_id_valid(record)
        trader_id_valid(record)
        price_valid(record)
        currency_valid(record)
        isin_valid(record)
        market_valid(record)
        trade_leg_valid(record)
        is_otc_valid(record)
        direction_valid(record)
        quantity_valid(record)
        created_timestamp_valid(record)


def contract_id_valid(record):
    pass


def booking_datetime_valid(record):
    pass


def trade_datetime_valid(record):
    pass


def value_datetime_valid(record):
    pass


def order_id_valid(record):
    pass


def account_id_valid(record):
    pass


def counterparty_id_valid(record):
    pass


def trader_id_valid(record):
    pass


def price_valid(record):
    pass


def currency_valid(record):
    pass


def isin_valid(record):
    pass


def market_valid(record):
    pass


def trade_leg_valid(record):
    pass


def is_otc_valid(record):
    pass


def direction_valid(record):
    pass


def quantity_valid(record):
    pass


def created_timestamp_valid(record):
    pass
