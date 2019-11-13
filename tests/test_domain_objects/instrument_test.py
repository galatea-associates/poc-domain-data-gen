import sys

sys.path.insert(0, 'tests/')
from utils import shared_tests as shared
from utils import helper_methods as helper


def test_instruments():
    """ Ensure all generated instrument attributes adhere to their
    specification. No dependencies. """

    records = helper.set_up_instrument_tests()
    shared.unique_ids(records, 'instrument')
    for record in records:
        shared.ric_valid(record)
        shared.isin_valid(record)
        sedol_valid(record)
        ticker_valid(record)
        shared.cusip_valid(record)
        asset_class_valid(record)
        country_of_issuance_valid(record)


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


def asset_class_valid(record):
    """ Asset class must equal 'stock' """
    asset_class = record['asset_class']
    assert asset_class == 'Stock'


def country_of_issuance_valid(record):
    """ country_of_issuance must be within the set as provided within
    exchanges database table """

    database = helper.create_db()
    countries_of_issuance = \
        database.retrieve_column_as_list("exchanges", "country_of_issuance")

    country_of_issuance = record['country_of_issuance']
    assert country_of_issuance in countries_of_issuance
