import random
from datetime import datetime

from domainobjects.generatable import Generatable


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

        self.countries_of_issuance = \
            self.retrieve_column("exchanges", "country_of_issuance")
        self.tickers = self.retrieve_column('tickers', "symbol")
        self.exchange_codes = self.retrieve_column("exchanges",
                                                   "exchange_code")
        records = []

        for i in range(start_id, start_id + record_count):
            record = self.generate_record(i)
            records.append(record)
            self.persist_record(
                [record['ric'], str(record['cusip']), str(record['isin'])]
            )

        self.persist_records("instruments")
        return records

    def generate_record(self, id):
        """ Generate a single instrument

        Parameters
        ----------
        id : int
            Current id of the instrument to generate, used as a pseudo
            exchange code to ensure uniquely generated instruments

        Returns
        -------
        dict
            A single back office position object
        """

        asset_class = self.generate_asset_class()
        ticker = self.generate_ticker()
        country_of_issuance = self.generate_country_of_issuance()
        exchange_code = self.generate_exchange_code()
        cusip = self.generate_random_integer(length=9)
        isin = self.generate_isin(country_of_issuance, cusip)
        ric = self.generate_ric(ticker, exchange_code)
        sedol = self.generate_random_integer(length=7)
        record = {
            'instrument_id': id,
            'ric': ric,
            'isin': isin,
            'sedol': sedol,
            'ticker': ticker,
            'cusip': cusip,
            'asset_class': asset_class,
            'country_of_issuance': country_of_issuance,
            'time_stamp': datetime.now()
        }
        record.update(self.get_dummy_fields_record())
        return record

    def generate_asset_class(self):
        """ Generate a predetermined asset class for instruments

        Returns
        -------
        String
            Asset class of an instrument will be 'Stock'
        """

        return 'Stock'

    def generate_country_of_issuance(self):
        """ Generate a random country of issuance

        Returns
        -------
        String
            Randomly selected country code from those in the cache
        """

        return random.choice(self.countries_of_issuance)

    def generate_ticker(self):
        """ Generate a random ticker

        Returns
        -------
        String
            Randomly selected ticker from those in the cache
        """

        return random.choice(self.tickers)

    def generate_exchange_code(self):
        """ Generate a random exchange code

        Returns
        -------
        String
            Randomly selected exchange code from those in the cache
        """

        return random.choice(self.exchange_codes)
