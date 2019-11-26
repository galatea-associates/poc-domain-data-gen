import sys
import datetime
sys.path.insert(0, 'tests/')
from utils import shared_tests as shared
from utils import helper_methods as helper


def test_front_office_position():
    """ Ensure all generated front office position attributes adhere to their
    specification. """
    records, domain_obj = helper.set_up_front_office_position_tests()
    for record in records:
        shared.attribute_quantity_valid('front_office_position', record, 6)
        as_of_date_valid(record)
        value_date_valid(record)
        account_id_valid(record, domain_obj)
        cusip_valid(record, domain_obj)
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


def account_id_valid(record, domain_obj):
    """ account id must exist in the database 'accounts' table """
    account_id = record['account_id']
    assert account_id in domain_obj.retrieve_column('accounts', 'account_id')


def cusip_valid(record, domain_obj):
    """ cusip must exist in the database 'instruments' table """
    cusip = record['cusip']
    assert cusip in domain_obj.retrieve_column('instruments', 'cusip')


def quantity_valid(record):
    """ quantity must be positive or negative and have magnitude less than
    or equal to 10000"""
    assert 1 <= abs(record['quantity']) <= 10000


def purpose_valid(record):
    """ purpose must be 'Outright' """
    assert record['purpose'] == 'Outright'
