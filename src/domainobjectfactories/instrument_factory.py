import random
from datetime import datetime

from domainobjectfactories.creatable import Creatable


class InstrumentFactory(Creatable):
    """ Class to create instruments. Create method creates a set amount
    of positions. Other creation methods included where instruments are the
    only domain object requiring these.
    """

    def create(self, record_count, start_id):
        """ Create a set number of instruments

        Parameters
        ----------
        record_count : int
            Number of instruments to create
        start_id : int
            Starting id to create from

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
            record = self.create_record(i)
            records.append(record)
            self.persist_record(
                [record['ric'], str(record['cusip']), str(record['isin']), str(record['country_of_issuance'])]
            )

        self.persist_records("instruments")
        return records

    def create_record(self, id):
        """ Create a single instrument

        Parameters
        ----------
        id : int
            Current id of the instrument to create, used as a pseudo
            exchange code to ensure uniquely created instruments

        Returns
        -------
        dict
            A single back office position object
        """

        asset_class = self.create_asset_class()
        ticker = self.create_ticker()
        country_of_issuance = self.create_country_of_issuance()
        exchange_code = self.create_exchange_code()
        cusip = self.create_random_integer(length=9)
        isin = self.create_isin(country_of_issuance, cusip)
        ric = self.create_ric(ticker, exchange_code)
        sedol = self.create_random_integer(length=7)
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

        for key, value in self.create_dummy_field_generator():
            record[key] = value

        return record

    def create_asset_class(self):
        """ Create a predetermined asset class for instruments

        Returns
        -------
        String
            Asset class of an instrument will be 'Stock'
        """

        return 'Stock'

    def create_country_of_issuance(self):
        """ Create a random country of issuance

        Returns
        -------
        String
            Randomly selected country code from those in the cache
        """

        return random.choice(self.countries_of_issuance)

    def create_ticker(self):
        """ Create a random ticker

        Returns
        -------
        String
            Randomly selected ticker from those in the cache
        """

        return random.choice(self.tickers)

    def create_exchange_code(self):
        """ Create a random exchange code

        Returns
        -------
        String
            Randomly selected exchange code from those in the cache
        """

        return random.choice(self.exchange_codes)
