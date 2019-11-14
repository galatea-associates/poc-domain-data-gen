from domainobjects.generatable import Generatable
from datetime import datetime
import random

class BackOfficePosition(Generatable):
    """ Class to generate back office positions. Generate method will generate
    a set amount of positions. Other generation methods included where back
    office positions are the only domain object requiring them. """

    BACK_OFFICE_ACCOUNT_TYPES = ['ICP']
    BACK_OFFICE_PURPOSES = ['Outright']

    def generate(self, record_count, start_id):
        """ Generate a set number of back office positions

        Parameters
        ----------
        record_count : int
            Number of back office positions to generate
        start_id : int
            Starting id to generate from

        Returns
        -------
        List
            Containing 'record_count' back office positions
        """

        self.instruments = self.retrieve_records('instruments')
        records = []

        for _ in range(start_id, start_id+record_count):
            records.append(self.generate_record())

        return records

    def generate_record(self):
        """ Generate a single back office position

        Returns
        -------
        dict
            A single back office position object
        """

        instrument = self.get_random_instrument()
        position_type = self.generate_position_type()
        knowledge_date = self.generate_knowledge_date()
        record = {
            'cusip': instrument['cusip'],
            'position_type': position_type,
            'knowledge_date': knowledge_date,
            'effective_date': self.generate_effective_date(
                                2, knowledge_date, position_type),
            'account': self.generate_account(
                account_types=self.BACK_OFFICE_ACCOUNT_TYPES
                ),
            'direction': self.generate_credit_debit(),
            'qty': self.generate_random_integer(),
            'purpose': self.generate_purpose(),
            'time_stamp': datetime.now(),
        }
        record.update(self.get_dummy_fields_record())
        return record

    def generate_purpose(self):
        """ Generate a purpose for a back office position

        Returns
        -------
        String
            Back office position purposes are always outright
        """

        return random.choice(self.BACK_OFFICE_PURPOSES)
