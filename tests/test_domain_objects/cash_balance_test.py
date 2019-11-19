import sys
sys.path.insert(0, 'tests/')
from utils import shared_tests as shared
from utils import helper_methods as helper


def test_cash_balance():
    """Ensure all generated cashflow attributes adhere to their
    specification. No Dependencies """

    records, domain_obj = helper.set_up_cash_balance_tests()
    for record in records:
        shared.attribute_quantity_valid('cash_balance', record, 5)
        shared.amount_valid(record)
        shared.currency_valid(record)
        shared.account_number_valid(record)
        shared.purpose_valid(record, domain_obj.CASH_BALANCE_PURPOSES)
