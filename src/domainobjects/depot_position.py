from domainobjects.generatable import Generatable
from datetime import datetime
import random
import string

class DepotPosition(Generatable):
    """ Class to generate depot positions. Generate method will generate a set
    amount of positions. Other generation method are included where depot
    positions are the only domain object requiring them. """

    DEPOT_POSITION_PURPOSES = ['Holdings', 'Seg']

    def generate(self, record_count, start_id):
        """ Generate a set number of depot positions

        Parameters
        ----------
        record_count : int
            Number of depot positions to generate
        start_id : int
            Starting id to generate from

        Returns
        -------
        List
            Containing 'record_count' depot positions
        """

        self.instruments = self.retrieve_records('instruments')

        records = []

        for _ in range(start_id, start_id+record_count):
            instrument = self.get_random_instrument()
            records.append(self.generate_record(instrument))

        return records

    def generate_record(self, instrument):
        """ Generate a single depot position

        Parameters
        ----------
        instrument : list
            Dictionary containing a partial record of an instrument, only
            containing information necessary to generate depot positions.

        Returns
        -------
        dict
            A single depot position object
        """

        position_type = self.generate_position_type()
        knowledge_date = self.generate_knowledge_date()
        record = {
            'isin': instrument['isin'],
            'knowledge_date': knowledge_date,
            'position_type': position_type,
            'effective_date': self.generate_effective_date(
                                2, knowledge_date, position_type),
            'account': self.generate_account(),
            'qty': self.generate_random_integer(),
            'purpose': self.generate_purpose(),
            'depot_id': self.generate_random_integer(length=5),
            'time_stamp': datetime.now()
        }
        record.update(self.get_dummy_fields_record())
        return record

    def generate_purpose(self):
        """ Generate a purpose for a depot position

        Returns
        -------
        String
            Depot position purposes are one of Holdings or Seg
        """
        return random.choice(self.DEPOT_POSITION_PURPOSES)
