import sys
import datetime
sys.path.insert(0, 'tests/')
from utils import shared_tests as shared
from utils import helper_methods as helper


def test_front_office_position():
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
    assert record['as_of_date'] == datetime.date.today()


def value_date_valid(record):
    value_date = record['value_date']
    today = datetime.date.today()
    day_after_tomorrow = today + datetime.timedelta(days=2)
    assert value_date in (today, day_after_tomorrow)


def account_id_valid(record, domain_obj):
    account_id = record['account_id']
    assert account_id in domain_obj.retrieve_column('accounts', 'account_id')


def cusip_valid(record, domain_obj):
    cusip = record['cusip']
    assert cusip in domain_obj.retrieve_column('instruments', 'cusip')


def quantity_valid(record):
    assert 1 <= abs(record['quantity']) <= 10000


def purpose_valid(record):
    assert record['purpose'] == 'Outright'
