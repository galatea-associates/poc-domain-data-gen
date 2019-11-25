import random
import datetime

from domainobjectfactories.creatable import Creatable


class FrontOfficePositionFactory(Creatable):
    """ Class to create front office positions. Create method will
    create a set amount of positions. Other creation methods included
    where front office positions are the only domain object requiring them.
    """

    def create(self, record_count, start_id):
        """ Create a set number of front office positions

        Parameters
        ----------
        record_count : int
            Number of front office positions to create
        start_id : int
            Starting id to create from

        Returns
        -------
        List
            Containing 'record_count' front office positions
        """

        records = []

        for _ in range(start_id, start_id + record_count):
            records.append(self.create_record())
        return records

    def create_record(self):
        """ Create a single front office position

        Returns
        -------
        dict
            A single front office position object
        """

        record = {
            'as_of_date': self.create_as_of_date(),
            'value_date': self.create_value_date(),
            'account_id': self.create_account_id(),
            'cusip': self.create_cusip(),
            'quantity': self.create_quantity(),
            'purpose': self.create_purpose()
        }

        for key, value in self.create_dummy_field_generator():
            record[key] = value

        return record

    @staticmethod
    def create_as_of_date():
        return datetime.date.today()

    @staticmethod
    def create_value_date():
        today = datetime.date.today()
        day_after_tomorrow = today + datetime.timedelta(days=2)
        return random.choice((today, day_after_tomorrow))

    def create_account_id(self):
        account = self.get_random_account()
        while account['account_type'] not in ('Client', 'Firm'):
            account = self.get_random_account()
        return account['account_id']

    def create_cusip(self):
        instrument = self.get_random_instrument()
        return instrument['cusip']

    def create_quantity(self):
        """ Return front office position quantity, being a positive or
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
    def create_purpose():
        """ Create a purpose for a front office position

        Returns
        -------
        String
            Front office position purposes are always outright
        """

        return 'Outright'
