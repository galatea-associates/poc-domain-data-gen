import random
import datetime

from domainobjectfactories.creatable import Creatable


class DepotPositionFactory(Creatable):
    """ Class to create depot positions. Create method will create a set
    amount of positions. Other creation method are included where depot
    positions are the only domain object requiring them. """

    DEPOT_POSITION_PURPOSES = ['Holdings', 'Seg', 'Pending Holdings']

    def create(self, record_count, start_id):
        """ Create a set number of depot positions

        Parameters
        ----------
        record_count : int
            Number of depot positions to create
        start_id : int
            Starting id to create from

        Returns
        -------
        List
            Containing 'record_count' depot positions
        """

        records = []

        for _ in range(start_id, start_id+record_count):
            records.append(self.create_record())

        return records

    def create_record(self):
        """ Create a single depot position

        Returns
        -------
        dict
            A single depot position object
        """

        isin, cusip, market = self.create_instrument_details()

        record = {
            'as_of_date': self.create_as_of_date(),
            'value_date': self.create_value_date(),
            'isin': isin,
            'cusip': cusip,
            'market': market,
            'depot_id': self.create_depot_id(),
            'purpose': self.create_purpose(),
            'quantity': self.create_quantity()
        }

        for key, value in self.create_dummy_field_generator():
            record[key] = value

        return record

    # TODO: check as of and value dates implemented correctly

    @staticmethod
    def create_as_of_date():
        """ Return the 'as of date', which must be the current date
        Returns
        -------
        Date
            Date object representing the current date
        """
        return datetime.date.today()

    @staticmethod
    def create_value_date():
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

    def create_instrument_details(self):
        instrument = self.get_random_instrument()
        isin = instrument['isin']
        cusip = instrument['cusip']
        market = instrument['market']
        return isin, cusip, market

    def get_depot_id(self):
        account = self.get_random_account()
        while account['account_type'] != 'Depot':
            account = self.get_random_account()
        return account['account_id']

    def create_purpose(self):
        """ Create a purpose for a depot position

        Returns
        -------
        String
            Depot position purposes are one of Holdings, Seg, or
            Pending Holdings
        """
        return random.choice(self.DEPOT_POSITION_PURPOSES)

    def create_quantity(self):
        return self.create_random_integer()
