import sys
import re
from datetime import datetime
sys.path.insert(0, 'tests/')
from utils import shared_tests as shared
from utils import helper_methods as helper


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
    is_valid = True
    try:
        # not assigned since we are only checking to see if ValueError raised
        datetime.strptime(date_string, "%Y%m%d")
    except ValueError:
        is_valid = False
    finally:
        assert is_valid


def opening_date_valid(record):
    """ Opening Date must be format YYYYMMDD with valid values for DD and MM
    """
    opening_date = record["opening_date"]
    date_valid(opening_date)


def closing_date_valid(record):
    """ Closing Date must be "Empty" or a date string of format YYYYMMDD with
    valid values for DD and MM and must represent a date on or after the
    Opening Date in the record """
    closing_date = record["closing_date"]
    pattern = "^[0-9]{8}$"  # matches any 8-digit integer
    if re.match(pattern, closing_date):
        date_valid(closing_date)
        opening_date = record["opening_date"]
        assert datetime.strptime(opening_date, "%Y%m%d") <= \
            datetime.strptime(closing_date, "%Y%m%d")
    else:
        assert closing_date == "Empty"
