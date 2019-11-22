import sys
import re
sys.path.insert(0, 'tests/')
from utils import shared_tests as shared
from utils import helper_methods as helper
from datetime import datetime


def test_accounts():
    """ Ensure all generated instrument attributes adhere to their
    specification. No dependencies. """
    records = helper.set_up_account_tests()
    shared.unique_ids(records, 'account')
    for record in records:
        shared.attribute_quantity_valid('account', record, 10)
        account_type_valid(record)
        account_purpose_valid(record)
        account_description_valid(record)
        account_status_valid(record)
        iban_valid(record)
        account_set_id_valid(record)
        legal_entity_id_valid(record)
        opening_date_valid(record)
        closing_date_valid(record)


def account_type_valid(record):
    """ Account type must be from the values specified """
    assert record['account_type'] in \
           ['Client', 'Firm', 'Counterparty', 'Depot']


def account_purpose_valid(record):
    """ Account purpose must be from the values specified """
    assert record['account_purpose'] in \
           ['Fully Paid', 'Financed', 'Stock Loan', 'Rehypo', 'Collateral']


def account_description_valid(record):
    """ Account description must be a 10 character string """
    account_description = record['account_description']
    assert shared.is_length(10, account_description)
    assert isinstance(account_description, str)


def account_status_valid(record):
    """ Account status must be 'Open' or 'Closed' """
    assert record['account_status'] in ['Open', 'Closed']


def iban_valid(record):
    """ IBAN must match the regex for one of the country formats used """
    GB_pattern = "^GB[0-9]{2}[A-Z]{4}[0-9]{14}$"
    CH_pattern = "^CH[0-9]{19}$"
    FR_pattern = "^FR[0-9]{22}[A-Z][0-9]{2}$"
    DE_pattern = "^DE[0-9]{20}$"
    SA_pattern = "^SA[0-9]{22}$"
    pattern = GB_pattern + "|" + CH_pattern + "|" + FR_pattern + "|" +\
        DE_pattern + "|" + SA_pattern
    iban = record['iban']
    assert re.match(pattern, iban)


def account_set_id_valid(record):
    """ Account set id must be a 10 character string """
    account_set_id = record['account_set_id']
    assert shared.is_length(10, account_set_id)
    assert isinstance(account_set_id, str)


def legal_entity_id_valid(record):
    """ legal entity id must be a 10 character string """
    legal_entity_id = record['legal_entity_id']
    assert shared.is_length(10, legal_entity_id)
    assert isinstance(legal_entity_id, str)


def date_valid(date_string):
    """ checks a string is format YYYYMMDD with valid values for DD and MM """
    pattern = "^[0-9]{8}$"
    assert re.match(pattern, date_string)
    month = date_string[4:6]
    assert int(month) in range(1, 13)
    day = date_string[6:]
    assert int(day) in range(1, 29)


def opening_date_valid(record):
    """ Opening Date must be format YYYYMMDD with valid values for DD and MM
    """
    opening_date = record["opening_date"]
    date_valid(opening_date)


def closing_date_valid(record):
    """ Closing Date must be format YYYYMMDD with valid values for DD and MM
    and must represent a date on or after the Opening Date in the record """
    closing_date = record["closing_date"]
    date_valid(closing_date)
    opening_date = record["opening_date"]
    o_year, o_month, o_day = int(opening_date[:4]), int(opening_date[4:6]),\
        int(opening_date[6:])
    c_year, c_month, c_day = int(closing_date[:4]), int(closing_date[4:6]),\
        int(closing_date[6:])
    assert datetime(o_year, o_month, o_day) <= datetime(c_year, c_month, c_day)
