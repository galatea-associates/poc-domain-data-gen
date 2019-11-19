import random
from datetime import datetime

from domainobjects.creatable import Creatable


class BackOfficePositionFactory(Creatable):
    """ Class to create back office positions. Create method will create
    a set amount of positions. Other creation methods included where back
    office positions are the only domain object requiring them. """

    BACK_OFFICE_ACCOUNT_TYPES = ['ICP']
    BACK_OFFICE_PURPOSES = ['Outright']

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

        self.instruments = self.retrieve_records('instruments')
        records = []

        for _ in range(start_id, start_id+record_count):
            records.append(self.create_record())

        return records

    def create_record(self):
        """ Create a single back office position

        Returns
        -------
        dict
            A single back office position object
        """

        instrument = self.get_random_instrument()
        position_type = self.create_position_type()
        knowledge_date = self.create_knowledge_date()
        record = {
            'cusip': instrument['cusip'],
            'position_type': position_type,
            'knowledge_date': knowledge_date,
            'effective_date': self.create_effective_date(
                                2, knowledge_date, position_type),
            'account': self.create_account(
                account_types=self.BACK_OFFICE_ACCOUNT_TYPES
                ),
            'direction': self.create_credit_debit(),
            'qty': self.create_random_integer(),
            'purpose': self.create_purpose(),
            'time_stamp': datetime.now(),
        }

        for key, value in self.create_dummy_field_generator():
            record[key] = value

        return record

    def create_purpose(self):
        """ Create a purpose for a back office position

        Returns
        -------
        String
            Back office position purposes are always outright
        """

        return random.choice(self.BACK_OFFICE_PURPOSES)
