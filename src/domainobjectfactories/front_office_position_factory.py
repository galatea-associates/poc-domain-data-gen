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
            records.append(self.__create_record())
        return records

    def __create_record(self):
        """ Create a single front office position

        Returns
        -------
        dict
            A single front office position object
        """

        record = {
            'as_of_date': self.__create_as_of_date(),
            'value_date': self.__create_value_date(),
            'account_id': self.__create_account_id(),
            'cusip': self.__create_cusip(),
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

    def __create_account_id(self):
        """ Return a account id from an account persisted in the database where
        account type is 'Client' or 'Firm'

        Returns
        -------
        String
            account id from the local database
        """
        account = self.get_random_record_with_valid_attribute(
            'accounts', 'account_type', ['Client', 'Firm']
        )
        account_id = account['account_id']
        return account_id

    def __create_cusip(self):
        """ Return a cusip from an instrument persisted in the database

        Returns
        -------
        String
            cusip from the local database
        """
        instrument = self.get_random_instrument()
        return instrument['cusip']

    def __create_quantity(self):
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
    def __create_purpose():
        """ Create a purpose for a front office position

        Returns
        -------
        String
            Front office position purposes are always outright
        """

        return 'Outright'
