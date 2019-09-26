from domainobjects.generatable import Generatable
from datetime import datetime
from utils.cache import Cache
import random

class Instrument(Generatable):
    """ Class to generate instruments. Generate method generates a set amount
    of positions. Other generation methods included where instruments are the
    only domain object requiring these.
    """

    def generate(self, record_count, start_id):
        """ Generate a set number of instruments

        Parameters
        ----------
        record_count : int
            Number of instruments to generate
        start_id : int
            Starting id to generate from

        Returns
        -------
        List
            Containing 'record_count' instruments 
        """

        cache = Cache()

        records = []

        for i in range(start_id, start_id+record_count):
            record = self.generate_record(i, cache)
            records.append(record)
            self.persist_record(
                [record['ric'], record['cusip'], record['isin']]
            )

        self.persist_records("instruments")
        return records

    def generate_record(self, id, cache):
        """ Generate a single instrument

        Parameters
        ----------
        id : int
            Current id of the instrument to generate, used as a pseudo
            exchange code to ensure uniquely generated instruments
        cache : dict
            Storeage medium for tickers and countries of issuance.

        Returns
        -------
        dict
            A single back office position object
        """

        asset_class = self.generate_asset_class()
        ticker = self.generate_ticker(cache)
        coi = self.generate_coi(cache)
        exchange_code = id
        cusip = str(self.generate_random_integer(length=9))
        isin = self.generate_isin(coi, cusip)
        ric = self.generate_ric(ticker, exchange_code)
        sedol = self.generate_random_integer(length=7)
        return {
                'instrument_id': id,
                'ric': ric,
                'isin': isin,
                'sedol': sedol,
                'ticker': ticker,
                'cusip': cusip,
                'asset_class': asset_class,
                'coi': coi,
                'time_stamp': datetime.now()
            }

    def generate_asset_class(self):
        """ Generate a predetermined asset class for instruments

        Returns
        -------
        String
            Asset class of an instrument will be 'Stock'
        """

        return 'Stock'

    def generate_coi(self, cache):
        """ Generate a random country of issuance

        Parameters
        ----------
        cache : dict
            Storeage medium for tickers and countries of issuance and exchange
            codes

        Returns
        -------
        String
            Randomly selected country code from those in the cache
        """

        return random.choice(cache.retrieve_from_cache('cois'))

    def generate_ticker(self, cache):
        """ Generate a random ticker

        Parameters
        ----------
        cache : dict
            Storeage medium for tickers and countries of issuance and exchange
            codes

        Returns
        -------
        String
            Randomly selected ticker from those in the cache
        """

        return random.choice(cache.retrieve_from_cache('tickers'))

    def generate_exchange_code(self, cache):
        """ Generate a random exchange code

        Parameters
        ----------
        cache : dict
            Storeage medium for tickers and countries of issuance and exchange
            codes

        Returns
        -------
        String
            Randomly selected exchange code from those in the cache
        """

        return random.choice(cache.retrieve_from_cache('exchange_codes'))
