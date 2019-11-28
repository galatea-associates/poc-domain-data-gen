import sys
import re

sys.path.insert(0, 'tests/')
from utils import shared_tests as shared
from utils import helper_methods as helper


def test_instruments():
    """ Ensure all generated instrument attributes adhere to their
    specification. No dependencies. """

    records = helper.set_up_instrument_tests()
    shared.unique_ids(records, 'instrument')
    for record in records:
        shared.attribute_quantity_valid('instrument', record, 20)
        shared.ric_valid(record)
        shared.isin_valid(record)
        sedol_valid(record)
        ticker_valid(record)
        shared.cusip_valid(record)
        valoren_valid(record)
        asset_class_valid(record)
        asset_subclass_valid(record)
        country_of_issuance_valid(record)
        shared.value_is_valid_market(record['primary_market'])
        shared.value_is_valid_market(record['market'])
        is_primary_listing_valid(record)
        figi_valid(record)
        issuer_name_valid(record)
        industry_classification_valid(record)


def sedol_valid(record):
    """ SEDOLs must both: be integers, and of length 7 """
    sedol = record['sedol']
    assert shared.is_int(sedol) and shared.is_length(7, sedol)


def ticker_valid(record):
    """ Ticker must be within the set as provided within tickers database
    table """

    database = helper.create_db()
    database_rows = database.retrieve("tickers")

    tickers = []
    for row in database_rows:
        tickers.append(row['symbol'])
    ticker = record['ticker']
    assert ticker in tickers


def valoren_valid(record):
    """"Valoren must be a number between 6 and 9 digits long"""
    valoren = record['valoren']
    assert shared.is_int(valoren) and (shared.is_length(6, valoren) or
                                       shared.is_length(7, valoren) or
                                       shared.is_length(8, valoren) or
                                       shared.is_length(9, valoren))


def quick_valid(record):
    """Quick must be a 4 digit number"""
    quick = record['quick']
    assert shared.is_int(quick) and shared.is_length(4, quick)


def sicovam_valid(record):
    """sicovam must be a 6 digit number"""
    sicovam = record['sicovam']
    assert shared.is_int(sicovam) and shared.is_length(6, sicovam)


def asset_class_valid(record):
    asset_class = record['asset_class']
    assert asset_class in ['Equity', 'Fund', 'Derivative']


def asset_subclass_valid(record):
    asset_class = record['asset_class']
    asset_subclass = record['asset_subclass']
    if asset_class == 'Equity':
        assert asset_subclass in ['Common', 'Preferred']
    if asset_class == 'Fund':
        assert asset_subclass in ['ETF', 'Mutual Fund']
    if asset_class == 'Derivative':
        assert asset_subclass in ['Right', 'Warrant']


def country_of_issuance_valid(record):
    """ country_of_issuance must be within the set as provided within
    exchanges database table """

    database = helper.create_db()
    countries_of_issuance = \
        database.retrieve_column_as_list("exchanges", "country_of_issuance")

    country_of_issuance = record['country_of_issuance']
    assert country_of_issuance in countries_of_issuance


def is_primary_listing_valid(record):
    is_primary_listing = record['is_primary_listing']
    assert type(is_primary_listing) == bool


def figi_valid(record):
    figi = record['figi']
    assert re.search('[A-Z][A-Z]', figi[:2])

    invalid_combinations = ['BS', 'BM', 'GG', 'GB', 'GH', 'KY', 'VG']
    assert figi[:2] not in invalid_combinations

    assert figi[2] == 'G'

    consonants = ['B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N',
                  'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'Y', 'Z']
    consonants_and_numbers = consonants + ['1', '2', '3', '4', '5', '6',
                                           '7', '8', '9']

    for char in figi[3:10]:
        assert char in consonants_and_numbers

    assert figi[11].isdigit()


def issuer_name_valid(record):
    assert re.match('^[A-Z0-9]{10}$', record['issuer_name'])


def industry_classification_valid(record):
    assert record['industry_classification'] in \
           ['MANUFACTURING', 'TELECOMS', 'FINANCIAL SERVICES', 'GROCERIES']
