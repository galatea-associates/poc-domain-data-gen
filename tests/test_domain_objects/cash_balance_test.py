import sys
from test_domain_objects import shared_tests as shared
from test_domain_objects import helper_methods as helper


sys.path.insert(0, 'tests/')


def test_cash_balance():
    """Ensure all generated cashflow attributes adhere to their
    specification. No Dependencies """

    records, domain_obj = helper.set_up_cash_balance_tests()
    for record in records:
        shared.amount_valid(record)
        shared.currency_valid(record)
        shared.account_number_valid(record)
        shared.purpose_valid(record, domain_obj.CASH_BALANCE_PURPOSES)
