from datetime import datetime, timedelta, timezone
import re
import sys

sys.path.insert(0, 'tests/')
from utils import shared_tests as shared
from utils import helper_methods as helper


def test_settlement_instructions():
    records, domain_obj = helper.set_up_settlement_instruction_tests()
    for record in records:
        shared.attribute_quantity_valid('settlement_instruction', record, 22)
        message_reference_valid(record)
        function_valid(record)
        shared.correct_datetime(record['message_creation_timestamp'])
        linked_message_valid(record)
        linkage_type_valid(record)
        shared.value_is_valid_market(record['place_of_trade'])
        shared.correct_datetime(record['trade_datetime'])
        shared.monetary_amount_valid\
            (record, field_name='deal_price', min=1, max=100000)
        shared.currency_valid(record)
        shared.isin_exists(record)
        shared.value_is_valid_market(record['place_of_listing'])
        quantity_valid(record)
        bic_valid(record['party_bic'])
        party_iban_valid(record, domain_obj)
        account_type_valid(record)
        bic_valid(record['safekeeper_bic'])
        settlement_type_valid(record)
        bic_valid(record['counterparty_bic'])
        counterparty_iban_valid(record, domain_obj)
        correct_settlement_date(record)
        valid_instruction_type(record)
        valid_status(record)


def message_reference_valid(record):
    assert re.match('^[A-Z0-9]{10}[0-9]+$', record['message_reference'])


def function_valid(record):
    assert record['function'] in ['CANCEL', 'NEW']


def linked_message_valid(record):
    assert (re.match('^[A-Z0-9]{10}[0-9]+$', record['message_reference']) or
            record['message_reference'] == 'EMPTY')


def linkage_type_valid(record):
    assert record['linkage_type'] in ['BEFORE', 'AFTER', 'WITH', 'INFO']


def quantity_valid(record):
    assert 1 <= record['quantity'] <= 10000


def bic_valid(bic):
    assert re.match('^[A-Z0-9]{10}$', bic)


def party_iban_valid(record, domain_obj):
    account_table = domain_obj.retrieve_records('accounts')
    details_in_database = False

    for account in account_table:
        if account['iban'] == record['party_iban'] and \
                account['account_type'] in ['Client', 'Firm']:
            details_in_database = True
            break

    assert details_in_database


def account_type_valid(record):
    assert record['account_type'] in ['SAFE', 'CASH']


def settlement_type_valid(record):
    assert record['settlement_type'] == 'Beneficial Ownership'


def counterparty_iban_valid(record, domain_obj):
    account_table = domain_obj.retrieve_records('accounts')
    details_in_database = False

    for account in account_table:
        if account['iban'] == record['counterparty_iban'] and \
                account['account_type'] == 'Counterparty':
            details_in_database = True
            break

    assert details_in_database


def correct_settlement_date(record):
    """Ensure that the string passed in has a date value that matches the
     current date in UTC with format YYYYMMDD"""
    day_after_tomorrow = datetime.now(timezone.utc).date() + timedelta(days=2)
    expected_settlement_date = day_after_tomorrow.strftime("%Y%m%d")
    assert record['settlement_date'] == expected_settlement_date


def valid_instruction_type(record):
    assert record['instruction_type'] in \
           ['DVP', 'RVP', 'DELIVERY FREE', 'RECEIVABLE FREE']


def valid_status(record):
    assert record['status'] in ['MATCHED', 'UNMATCHED']
