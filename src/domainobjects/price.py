from domainobjects.generatable import Generatable
from datetime import datetime
import random

class Price(Generatable):
    """ Class to generate prices. Generate method will generate a set amount
    of prices. """

    def generate(self, record_count, start_id):
        """ Generate a set number of prices

        Parameters
        ----------
        record_count : int
            Number of prices to generate
        start_id : int
            Starting id to generate from

        Returns
        -------
        List
            Containing 'record_count' prices
        """

        records = []
        self.instruments = self.retrieve_records('instruments')

        for _ in range(start_id, start_id+record_count):
            record = self.generate_record()
            records.append(record)

        return records

    def generate_record(self):
        """ Generate a single price

        Returns
        -------
        dict
            A single price object
        """

        instrument = self.get_random_instrument()
        return {
                'ric': instrument['ric'],
                'price': self.generate_random_decimal(),
                'currency': self.generate_currency(),
                'time_stamp': datetime.now()
            }
