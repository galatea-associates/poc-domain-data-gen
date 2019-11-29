import sys
import datetime
sys.path.insert(0, 'tests/')
from utils import shared_tests as shared
from utils import helper_methods as helper


def test_depot_position():
    records, domain_obj = helper.set_up_depot_position_tests()
    for record in records:
        shared.attribute_quantity_valid('depot_position', record, 8)
        as_of_date_valid(record)
        value_date_valid(record)
        instrument_details_valid(record, domain_obj)
        depot_id_valid(record, domain_obj)
        purpose_valid(record)
        quantity_valid(record)


def as_of_date_valid(record):
    """ as of date must be the current date """
    assert record['as_of_date'] == datetime.date.today()


def value_date_valid(record):
    """ value date must be either the current date or 2 days later """
    value_date = record['value_date']
    today = datetime.date.today()
    day_after_tomorrow = today + datetime.timedelta(days=2)
    assert value_date in (today, day_after_tomorrow)


def instrument_details_valid(record, domain_obj):
    """ isin, cusip and market must all match to one instrument record in the
    local database """
    isin, cusip, market = record['isin'], record['cusip'], record['market']
    instrument_table = domain_obj.retrieve_records('instruments')
    details_in_database = False
    for instrument in instrument_table:
        if instrument['isin'] == isin and instrument['cusip'] == cusip and \
                instrument['market'] == market:
            details_in_database = True
            break
    assert details_in_database


def depot_id_valid(record, domain_obj):
    """ depot id must match to the account id of an account from the local
    database that has account type 'Depot' """
    depot_id = record['depot_id']
    account_table = domain_obj.retrieve_records('accounts')
    details_in_database = False
    for account in account_table:
        if account['account_type'] == 'Depot' \
                and account['account_id'] == depot_id:
            details_in_database = True
            break
    assert details_in_database


def purpose_valid(record):
    """ purpose must be in the values specified """
    assert record['purpose'] in ['Holdings', 'Seg', 'Pending Holdings']


def quantity_valid(record):
    """ quantity must be a positive integer not more than 10000 """
    assert 0 < record['quantity'] <= 10000
