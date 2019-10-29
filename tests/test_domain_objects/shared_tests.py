import sys, pytest
sys.path.insert(0, 'src/')
from datetime import datetime, timedelta

from test_domain_objects import helper_methods as helper
from utils.cache import Cache
from utils.sqlite_database import Sqlite_Database
from domainobjects import instrument

####################
### Shared Tests ###
####################

# Access to defined constant lists in the parent class
# generatable, otherwise uninstantiable as it is abstract
domain_obj = instrument.Instrument(None)

def attribute_exists(value, attribute, table):
    stored = helper.query_db(table, attribute)
    assert value in stored

def swap_contract_id_exists(record):
    swap_contract_ids = helper.query_db('swap_contracts', 'id')
    swap_contract_id = record['swap_contract_id']
    assert swap_contract_id in swap_contract_ids

def cusip_exists(record):
    """ Ensure the generated cusip is of an existing instrument """
    cusips = helper.query_db('instruments', 'cusip')
    assert record['cusip'] in cusips

def cusip_valid(record):
    """ CUSIPs must both: be integers, and of length 9 """
    cusip = record['cusip']
    assert is_int(cusip) and is_length(9, cusip)

def isin_exists(record):
    isins = helper.query_db('instruments', 'isin')
    assert record['isin'] in isins

def isin_valid(record):
    """ Valid ISIN is in format '"Country Of Issuance ""CUSIP""4"' """
    country_of_issuance = record['country_of_issuance']
    cusip = str(record['cusip'])
    expected_isin = country_of_issuance + cusip + '4'
    assert record['isin'] == expected_isin

def ric_exists(record):
    rics = helper.query_db('instruments', 'ric')
    ric = record['ric']
    assert ric in rics

def ric_valid(record):
    """ RIC Formatting should be a ticker followed by an exchange code.
    In this use case, exchange codes are currently integers. This test
    will require updating once this generation approach changes to real-world
    exchange codes. """
    ric = record['ric']
    ticker = record['ticker']
    id = str(record['instrument_id'])
    assert valid_ric(ticker, ric, id)

def valid_ric(ticker, ric, id):
    """ Valid RIC is in format '"ticker"."id"' """
    split_ric = ric.split('.')
    ticker_ = split_ric[0]
    id_ = split_ric[1]
    return ticker == ticker_ and id == id_

def unique_ids(records, object_name):
    id_set = set()
    id_field_name = object_name+'_id'

    for record in records:
            id_set.add(record[id_field_name])
    assert len(records) == len(id_set)

def dummy_fields_valid(record, object_name):
    partial_field_name = object_name+'_field'
    dummy_field_names = get_dummy_field_names(record, partial_field_name)

    for dummy_field in dummy_field_names:
        if not is_length(10, record[dummy_field]):
            assert False
    assert True

def get_dummy_field_names(record, partial_field_name):
    dummy_field_names = []
    for column_name in record.keys():
        if partial_field_name in column_name:
            dummy_field_names.append(column_name)
    return dummy_field_names

def long_short_valid(record):
    long_short_values = domain_obj.LONG_SHORT
    long_short_value = record['long_short']
    assert long_short_value in long_short_values

def purpose_valid(record, purposes):
    purpose = record['purpose']
    assert purpose in purposes

def account_number_valid(record):
    account_number = record['account_num']
    assert is_int(account_number) and is_length(8, account_number)

def currency_valid(record):
    cache = Cache()
    currencies = cache.retrieve_from_cache('currencies')
    currency = record['currency']
    assert currency in currencies

def amount_valid(record):
    amount = record['amount']
    assert 1 <= amount <= 10000

def quantity_valid(record, long_short='Long'):
    quantity = record['qty']
    if (long_short == 'Long'):
        assert 1 <= quantity <= 10000
    else:
        assert -10000 <= quantity <= -1

def direction_valid(record):
    assert record['direction'] in domain_obj.CREDIT_DEBIT

def account_valid(record, account_types):
    assert record['account'][:3] in account_types

def position_type_valid(record):
    domain_object = instrument.Instrument(None)
    position_types = domain_object.POSITION_TYPES
    assert record['position_type'] in position_types

def knowledge_date_valid(record):
    """ Ensure the knowledge date generated is todays date. 
    Hours/Minutes/Seconds/Milliseconds have been ommitted. """
    today = datetime.today().strftime("%Y-%m-%d")
    gen_date = record['knowledge_date'].strftime("%Y-%m-%d")
    assert gen_date == today

def settlement_position_effective_date_valid(record):
    """ Effective date is the same as knowledge for settlement """
    knowledge_date = record['knowledge_date']
    effective_date = record['effective_date']
    assert effective_date == knowledge_date

def trade_position_effective_date_valid(record):
    """ Effective date is two days in the future for trade date positions """
    knowledge_date = record['knowledge_date']
    effective_date = record['effective_date']
    assert effective_date == knowledge_date + timedelta(days=2)

def price_valid(record):
    """ Random float between 10 and 10,000 to 2 d.p """
    price = record['price']
    string_price = str(price)
    decimal = string_price.split(".")[1]
    assert 10 < price < 10000 and len(decimal) <= 2

#######################
### General Methods ###
#######################

def is_int(obj):
    return type(obj) == int

def is_length(length, obj):
    obj = str(obj)
    return len(obj) == length

def contains_numbers(string):
    return any(char.isdigit() for char in string)