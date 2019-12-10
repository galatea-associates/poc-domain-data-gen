import itertools
import random
from datetime import datetime, timezone

from domainobjectfactories.creatable import Creatable


class InstrumentFactory(Creatable):
    """ Class to create instruments. Create method creates a set amount
    of positions. Other creation methods included where instruments are the
    only domain object requiring these.
    """

    ASSET_CLASS_TO_SUBCLASS = {'Equity': ['Common', 'Preferred'],
                               'Fund': ['ETF', 'Mutual Fund'],
                               'Derivative': ['Right', 'Warrant']}

    INDUSTRY_CLASSIFICATIONS = \
        ['MANUFACTURING', 'TELECOMS', 'FINANCIAL SERVICES', 'GROCERIES']

    def create(self, record_count, start_id, lock=None):
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

        lock.acquire()
        self.tickers = self.retrieve_column('tickers', "symbol")
        lock.release()

        records = []

        for i in range(start_id, start_id + record_count):
            record = self.__create_record(i)
            records.append(record)
            self.persist_record(
                [str(record['instrument_id']),
                 record['ric'],
                 str(record['cusip']),
                 str(record['isin']),
                 str(record['market'])]
            )

        self.persist_records("instruments")
        return records

    def __create_record(self, id):
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

        ticker = self.__create_ticker()
        random_exchanges_row = self.get_random_row('exchanges')
        country_of_issuance = \
            self.__create_country_of_issuance(random_exchanges_row)
        exchange_code = self.__create_exchange_code(random_exchanges_row)
        ric = self.create_ric(ticker, exchange_code)
        cusip = self.create_random_integer(length=9)
        isin = self.create_isin(country_of_issuance, cusip)
        sedol = self.create_random_integer(length=7)
        valoren = self.create_random_integer(100000,
                                             999999999)
        quick = self.create_random_integer(length=4)
        sicovam = self.create_random_integer(length=6)
        asset_class = self.__create_asset_class()
        asset_subclass = self.__create_asset_sub_class(asset_class)
        primary_market = self.__get_market()
        market = self.__get_market()
        is_primary_listing = primary_market == market
        figi = self.__create_figi()
        issuer_name = self.create_random_string(10)
        industry_classification = self.__get_industry_classification()

        record = {
            'instrument_id': id,
            'ric': ric,
            'isin': isin,
            'sedol': sedol,
            'ticker': ticker,
            'cusip': cusip,
            'valoren': valoren,
            'quick': quick,
            'sicovam': sicovam,
            'asset_class': asset_class,
            'asset_subclass': asset_subclass,
            'country_of_issuance': country_of_issuance,
            'primary_market': primary_market,
            'market': market,
            'is_primary_listing': is_primary_listing,
            'figi': figi,
            'issuer_name': issuer_name,
            'industry_classification': industry_classification,
            'created_timestamp': datetime.now(timezone.utc),
            'last_updated_time_stamp': datetime.now(timezone.utc)
        }

        for key, value in self.create_dummy_field_generator():
            record[key] = value

        return record

    def __create_asset_class(self):
        """ Create a predetermined asset class for instruments

        Returns
        -------
        String
            Asset class of an instrument will be one of
            'Stock', 'Equity', 'Index' or 'Derivative'
        """

        return random.choice(list(self.ASSET_CLASS_TO_SUBCLASS.keys()))

    def __create_asset_sub_class(self, asset_class):
        """ Create a predetermined asset sub-class for instruments

        Returns
        -------
        String
            Asset sub-class of an instrument depends on its asset class
        """

        return random.choice(self.ASSET_CLASS_TO_SUBCLASS[asset_class])

    def __get_market(self):
        """Select a random country to be market

        Returns
        -------
        String
            Randomly selected country selected from database
        """
        return self.get_random_row('exchanges')['exchange_code']

    @staticmethod
    def __create_country_of_issuance(random_exchanges_row):
        """ Select a random country of issuance

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

    def __create_ticker(self):
        """ Create a random ticker

        Returns
        -------
        String
            Randomly selected ticker from those in the database
        """

        return random.choice(self.tickers)

    @staticmethod
    def __create_exchange_code(random_exchanges_row):
        """ Select a random exchange code

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

    def __create_issuer_name(self):
        """Create a random 10 character issuer name

        Returns
        -------
        String
            Randomly generate a ten character string to be issuer name
        """
        return self.create_random_string(length=10, include_numbers=False)

    @staticmethod
    def __create_figi():
        """Create a random valid FIGI

        Returns
        -------
        String
            Randomly generate a FIGI
        """

        consonants = ['B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N',
                      'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'Y', 'Z']
        consonants_and_numbers = consonants + ['1', '2', '3', '4', '5', '6',
                                               '7', '8', '9']

        random.shuffle(consonants)
        combination_generator = map(''.join,
                                    itertools.permutations(consonants, 2))
        invalid_combinations = ['BS', 'BM', 'GG', 'GB', 'GH', 'KY', 'VG']

        while True:
            combination = next(combination_generator)
            if combination not in invalid_combinations:
                break

        character_three = 'G'

        characters_four_to_eleven = \
            random.choices(consonants_and_numbers, k=8)

        # TODO Currently the final digit is being randomly generated,
        #  whereas in a true FIGI it is based on the preceding characters
        character_twelve = str(random.randint(0, 9))

        return combination + character_three + ''.join(
            characters_four_to_eleven) + character_twelve

    def __get_industry_classification(self):
        """Randomly select an industry classification

        Returns
        -------
        String
            A randomly chosen industry classification
        """
        return random.choice(self.INDUSTRY_CLASSIFICATIONS)
