import sys
from datetime import datetime, timezone, timedelta
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
        shared.currency_valid(record)
        instrument_details_valid(record)
        trade_leg_valid(record)
        is_otc_valid(record)
        direction_valid(record)
        quantity_valid(record)
        created_timestamp_valid(record)


def contract_id_valid(record):
    """ contract id must be a 10 character string """
    contract_id = record['contract_id']
    assert shared.is_length(10, contract_id)
    assert isinstance(contract_id, str)


def booking_datetime_valid(record):
    """ booking datetime must be a time within the current date in UTC """
    booking_datetime = record['booking_datetime']
    assert booking_datetime.date() == datetime.now(timezone.utc).date()


def trade_datetime_valid(record):
    """ trade datetime must be a time within the current date in UTC """
    trade_datetime = record['trade_datetime']
    assert trade_datetime.date() == datetime.now(timezone.utc).date()


def value_datetime_valid(record):
    """ booking datetime must be exactly 1 minute past midgnight on the
    morning of the day after the current date in UTC """
    value_datetime = record['value_datetime']
    assert value_datetime.date() == datetime.now(timezone.utc).date() + \
        timedelta(days=2)
    assert value_datetime.hour == 0
    assert value_datetime.minute == 1
    assert value_datetime.second == 0
    assert value_datetime.microsecond == 0


def order_id_valid(record):
    """ order id must be a positive integer between 1 and 10000 inclusive"""
    assert 1 <= record['order_id'] <= 10000


def account_id_valid(record):
    """ account id must match to a row in the accounts database table with
    account type of 'Client' or 'Firm'"""
    account_id = record['account_id']
    account_table = shared.domain_obj.retrieve_records('accounts')
    details_in_database = False
    for account in account_table:
        if account['account_id'] == account_id and \
                account['account_type'] in ['Client', 'Firm']:
            details_in_database = True
            break
    assert details_in_database


def counterparty_id_valid(record):
    """ counterparty id must match an account in the accounts database table
    of account type 'Counterparty'"""
    counterparty_id = record['counterparty_id']
    account_table = shared.domain_obj.retrieve_records('accounts')
    details_in_database = False
    for account in account_table:
        if account['account_id'] == counterparty_id and \
                account['account_type'] == 'Counterparty':
            details_in_database = True
            break
    assert details_in_database


def trader_id_valid(record):
    """ trader id must be a 10 character string """
    trader_id = record['trader_id']
    assert shared.is_length(10, trader_id)
    assert isinstance(trader_id, str)


def price_valid(record):
    """ price must be a float with 1 or 2 decimal places """
    price = record['price']
    assert isinstance(price, float)
    price_string = str(price)
    decimal_point_position = price_string.find('.')
    assert len(price_string) - decimal_point_position


def instrument_details_valid(record):
    """ isin and market must bot come from the same row in the instruments
    database table """
    isin = record['isin']
    market = record['market']
    instrument_table = shared.domain_obj.retrieve_records('instruments')
    details_in_database = False
    for instrument in instrument_table:
        if instrument['isin'] == isin and \
                instrument['market'] == market:
            details_in_database = True
            break
    assert details_in_database


def trade_leg_valid(record):
    """ trade leg must be one of the values specified"""
    assert record['trade_leg'] in ["EMPTY", "1", "2"]


def is_otc_valid(record):
    """ otc valid must be True or False"""
    assert record['is_otc'] in [True, False]


def direction_valid(record):
    """ direction must be one of the values specified """
    assert record['direction'] in ['BUY', 'SELL']


def quantity_valid(record):
    """ quantity must be positive and have magnitude less than or equal to
    10000"""
    assert 1 <= record['quantity'] <= 10000


def created_timestamp_valid(record):
    """ created timestamp must be a time within the current date in UTC """
    created_timestamp = record['created_timestamp']
    assert created_timestamp.date() == datetime.now(timezone.utc).date()
