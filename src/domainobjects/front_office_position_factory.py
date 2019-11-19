import random
from datetime import datetime

from domainobjects.creatable import Creatable


class FrontOfficePositionFactory(Creatable):
    """ Class to create front office positions. Create method will
    create a set amount of positions. Other creation methods included
    where front office positions are the only domain object requiring them.
    """

    FRONT_OFFICE_POSITION_PURPOSES = ['Outright']

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

        self.instruments = self.retrieve_records('instruments')

        records = []

        for _ in range(start_id, start_id + record_count):
            instrument = self.get_random_instrument()
            records.append(self.create_record(instrument))
        return records

    def create_record(self, instrument):
        """ Create a single front office position

        Parameters
        ----------
        instrument : list
            Dictionary containing a partial record of an instrument, only
            containing information necessary to create depot positions.

        Returns
        -------
        dict
            A single front office position object
        """
        position_type = self.create_position_type()
        knowledge_date = self.create_knowledge_date()
        record = {
            'ric': instrument['ric'],
            'position_type': position_type,
            'knowledge_date': knowledge_date,
            'effective_date': self.create_effective_date(
                2, knowledge_date, position_type),
            'account': self.create_account(),
            'direction': self.create_credit_debit(),
            'qty': self.create_random_integer(),
            'purpose': self.create_purpose(),
            'time_stamp': datetime.now()
        }

        for key, value in self.create_dummy_field_generator():
            record[key] = value

        return record

    def create_purpose(self):
        """ Create a purpose for a front office position

        Returns
        -------
        String
            Front office position purposes are always outright
        """

        return random.choice(self.FRONT_OFFICE_POSITION_PURPOSES)
