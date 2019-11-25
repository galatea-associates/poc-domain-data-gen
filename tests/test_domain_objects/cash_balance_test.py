import sys
import datetime
sys.path.insert(0, 'tests/')
from utils import shared_tests as shared
from utils import helper_methods as helper


def test_cash_balance():
    """Ensure all generated cashflow attributes adhere to their
    specification. No Dependencies """

    records, domain_obj = helper.set_up_cash_balance_tests()
    accounts_table = domain_obj.retrieve_records('accounts')
    for record in records:
        shared.attribute_quantity_valid('cash_balance', record, 6)
        as_of_date_valid(record)
        shared.amount_valid(record)
        shared.currency_valid(record)
        account_details_valid(record, accounts_table)
        shared.purpose_valid(record, domain_obj.CASH_BALANCE_PURPOSES)


def as_of_date_valid(record):
    """ as of date must be represent either the current date or the date
    in 2 days time """
    as_of_date = record['as_of_date']
    today = datetime.date.today()
    day_after_tomorrow = today + datetime.timedelta(days=2)
    assert as_of_date in (today, day_after_tomorrow)


def account_details_valid(record, accounts_table):
    """" account_id and account_owner must be from the same database record
    and represent a valid account (either 'Client' or 'Firm') """
    account_id, account_owner = record['account_id'], record['account_owner']
    assert account_owner in ('Firm', 'Client')

    details_in_database = False
    for row in accounts_table:
        if row['account_id'] == account_id and \
                row['account_type'] == account_owner:
            details_in_database = True
    assert details_in_database

