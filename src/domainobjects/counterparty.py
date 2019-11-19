from domainobjects.generatable import Generatable
import random
import string
from datetime import datetime

class Counterparty(Generatable):
    """ A class to generate counterparties. Generate method will generate a
    set amount of positions. """

    def generate(self, record_count, start_id):
        """ Generate a set number of counterparties.

        Parameters
        ----------
        record_count : int
            Number of counterparties to generate
        start_id : int
            Starting id to generate from

        Returns
        -------
        List
            Containing 'record_count' counterparties
        """

        records = []

        for i in range(start_id, record_count+start_id):
            records.append(self.get_record(i))
            self.persist_record([str(i)])

        self.persist_records("counterparties")
        return records

    def get_record(self, current_id):
        """ Generate a single counterparty record

        Parameters
        ----------
        current_id : int
            Current id of the counterparty being generated

        Returns
        -------
        dict
            A single counterparty objects
        """

        record = {
            'counterparty_id': current_id,
            'book': self.generate_random_string(5, include_numbers=False),
            'time_stamp': datetime.now()
        }

        for key, value in self.get_dummy_field_generator():
            record[key] = value

        return record
