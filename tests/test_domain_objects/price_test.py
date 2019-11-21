import sys

from domainobjectfactories.price_factory import PriceFactory

sys.path.insert(0, 'tests/')
from utils import shared_tests as shared
from utils import helper_methods as helper


def test_prices():
    records = helper.set_up_price_tests()
    for record in records:
        shared.attribute_quantity_valid('price', record, 4)
        shared.ric_exists(record)
        shared.price_valid(record)
        shared.currency_valid(record)
        currency_correct(record)


# todo This will need to be changed, we expect that in the MVP the unique
#  identifier for instruments will be InstrumentId rather than RIC
def currency_correct(record):
    database = helper.create_db()
    instrument_with_matching_ric = database.retrieve_on_matching_value(
        "instruments", "ric", record['ric'])
    assert (len(instrument_with_matching_ric) < 1), \
        "RIC should uniquely identify an instrument, but there are multiple" \
        " instruments with RIC " + record['ric']

    country_of_issuance = \
        instrument_with_matching_ric[0]['country_of_issuance']
    assert record['currency'] == \
           PriceFactory.country_of_issuance_to_currency[country_of_issuance]
