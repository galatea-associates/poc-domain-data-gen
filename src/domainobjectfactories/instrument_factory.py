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

        self.tickers = self.retrieve_column('tickers', "symbol")

        records = []

        for i in range(start_id, start_id + record_count):
            record = self.create_record(i)
            records.append(record)
            self.persist_record(
                [record['ric'], str(record['cusip']), str(record['isin'])]
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
        random_exchanges_row = self.get_random_row('exchanges')
        country_of_issuance = \
            self.__create_country_of_issuance(random_exchanges_row)
        exchange_code = self.__create_exchange_code(random_exchanges_row)
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

    def __create_country_of_issuance(self, random_exchanges_row):
        """ Create a random country of issuance

        Returns
        -------
        String
            Select country of issuance field from the randomly selected row
            from the exchanges table
        """
        assert ('country_of_issuance' in random_exchanges_row.keys()), \
            f"country_of_issuance not present in row.  Fields are: " \
            f"{random_exchanges_row.keys()}"
        return random_exchanges_row['country_of_issuance']

    def create_ticker(self):
        """ Create a random ticker

        Returns
        -------
        String
            Randomly selected ticker from those in the cache
        """

        return random.choice(self.tickers)

    def __create_exchange_code(self, random_exchanges_row):
        """ Create a random exchange code

        Returns
        -------
        String
            Select exchange code field from the randomly selected row from the
            exchanges table
        """

        assert ('exchange_code' in random_exchanges_row.keys()), \
            f"exchange_code not present in row.  Fields are: " \
            f"{random_exchanges_row.keys()}"
        return random_exchanges_row['exchange_code']
