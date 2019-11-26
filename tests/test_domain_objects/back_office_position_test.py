import sys
import datetime
sys.path.insert(0, 'tests/')
from utils import shared_tests as shared
from utils import helper_methods as helper


def test_back_office_positions():
    """ Ensure all generated back office position attributes adhere to their
    specification. """

    records, domain_obj = helper.set_up_back_office_position_tests()
    for record in records:
        shared.attribute_quantity_valid('back_office_position', record, 9)
        as_of_date_valid(record)
        value_date_valid(record)
        ledger_valid(record)
        instrument_details_valid(record, domain_obj)
        account_details_valid(record, domain_obj)
        quantity_valid(record)
        purpose_valid(record)


def as_of_date_valid(record):
    """ as of date must be the current date """
    assert record['as_of_date'] == datetime.date.today()


def value_date_valid(record):
    """ value date must be either the current date or 2 days later """
    value_date = record['value_date']
    today = datetime.date.today()
    day_after_tomorrow = today + datetime.timedelta(days=2)
    assert value_date in (today, day_after_tomorrow)


def ledger_valid(record):
    assert record['ledger'] in ['TD', 'SD']


def instrument_details_valid(record, domain_obj):
    instrument_id, isin = record['instrument_id'], record['isin']
    instrument_table = domain_obj.retrieve_records('instruments')
    details_in_database = False
    for instrument in instrument_table:
        if instrument['instrument_id'] == instrument_id and \
                instrument['isin'] == isin:
            details_in_database = True
            break
    assert details_in_database


def account_details_valid(record, domain_obj):
    account_id, account_type = record['account_id'], record['account_type']
    account_table = domain_obj.retrieve_records('accounts')
    details_in_database = False
    for account in account_table:
        if account['account_id'] == account_id and \
                account['account_type'] == account_type:
            details_in_database = True
            break
    assert details_in_database


def quantity_valid(record):
    assert abs(record['quantity']) <= 10000


def purpose_valid(record):
    assert record['purpose'] == 'Outright'
