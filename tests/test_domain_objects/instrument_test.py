import sys
import pytest
from utils.cache import Cache
from test_domain_objects import shared_tests as shared
from test_domain_objects import helper_methods as helper


sys.path.insert(0, 'tests/')
sys.path.insert(0, 'src/')


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
        coi_valid(record)


def sedol_valid(record):
    """ SEDOLs must both: be integers, and of length 7 """
    sedol = record['sedol']
    assert shared.is_int(sedol)\
        and shared.is_length(7, sedol)


def ticker_valid(record):
    """ Ticker must be within the set as provided within cache """
    cache = Cache()
    tickers = cache.retrieve_from_cache('tickers')
    ticker = record['ticker']
    assert ticker in tickers


def asset_class_valid(record):
    """ Asset class must equal 'stock' """
    asset_class = record['asset_class']
    assert asset_class == 'Stock'


def coi_valid(record):
    """ COI must be within the set as provided within cache """
    cache = Cache()
    cois = cache.retrieve_from_cache('cois')
    coi = record['coi']
    assert coi in cois
