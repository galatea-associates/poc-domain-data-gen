import random
import datetime

from domainobjectfactories.creatable import Creatable


class BackOfficePositionFactory(Creatable):
    """ Class to create back office positions. Create method will create
    a set amount of positions. Other creation methods included where back
    office positions are the only domain object requiring them. """

    LEDGERS = ['TD', 'SD']

    def create(self, record_count, start_id):
        """ Create a set number of back office positions

        Parameters
        ----------
        record_count : int
            Number of back office positions to create
        start_id : int
            Starting id to create from

        Returns
        -------
        List
            Containing 'record_count' back office positions
        """

        records = []

        for _ in range(start_id, start_id+record_count):
            records.append(self.__create_record())

        return records

    def __create_record(self):
        """ Create a single back office position

        Returns
        -------
        dict
            A single back office position object
        """

        instrument_id, isin = self.__create_instrument_details()
        account_id, account_type = self.__create_account_details()

        record = {
            'as_of_date': self.__create_as_of_date(),
            'value_date': self.__create_value_date(),
            'ledger': self.__create_ledger(),
            'instrument_id': instrument_id,
            'isin': isin,
            'account_id': account_id,
            'account_type': account_type,
            'quantity': self.__create_quantity(),
            'purpose': self.__create_purpose()
        }

        for key, value in self.create_dummy_field_generator():
            record[key] = value

        return record

    @staticmethod
    def __create_as_of_date():
        """ Return the 'as of date', which must be the current date
        Returns
        -------
        Date
            Date object representing the current date
        """
        return datetime.date.today()

    @staticmethod
    def __create_value_date():
        """ Return the 'value date', which must be today or in 2 days time
        Returns
        -------
        Date
            Date object representing the current date or the date in 2 days
            time
        """
        today = datetime.date.today()
        day_after_tomorrow = today + datetime.timedelta(days=2)
        return random.choice((today, day_after_tomorrow))

    def __create_ledger(self):
        return random.choice(self.LEDGERS)

    def __create_instrument_details(self):
        instrument = self.get_random_instrument()
        instrument_id = instrument['instrument_id']
        isin = instrument['isin']
        return instrument_id, isin

    def __create_account_details(self):
        account = self.get_random_account()
        while account['account_type'] not in \
                ['Client', 'Firm', 'Counterparty']:
            account = self.get_random_account()
        account_id = account['account_id']
        account_type = account['account_type']
        return account_id, account_type

    def __create_quantity(self):
        """ Return back office position quantity, being a positive or
        negative integer with absolute value not greater than 10000
        Returns
        -------
        int
            positive or negative integer with magnitude < 10000
        """
        return self.create_random_integer(
            negative=random.choice(self.TRUE_FALSE)
        )

    @staticmethod
    def __create_purpose():
        """ Create a purpose for a back office position

        Returns
        -------
        String
            Back office position purposes are always outright
        """

        return "Outright"
