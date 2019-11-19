from domainobjects.creatable import Creatable
from datetime import datetime
import random
import string

class DepotPositionFactory(Creatable):
    """ Class to create depot positions. Create method will create a set
    amount of positions. Other creation method are included where depot
    positions are the only domain object requiring them. """

    DEPOT_POSITION_PURPOSES = ['Holdings', 'Seg']

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

        self.instruments = self.retrieve_records('instruments')

        records = []

        for _ in range(start_id, start_id+record_count):
            instrument = self.get_random_instrument()
            records.append(self.create_record(instrument))

        return records

    def create_record(self, instrument):
        """ Create a single depot position

        Parameters
        ----------
        instrument : list
            Dictionary containing a partial record of an instrument, only
            containing information necessary to create depot positions.

        Returns
        -------
        dict
            A single depot position object
        """

        position_type = self.create_position_type()
        knowledge_date = self.create_knowledge_date()
        record = {
            'isin': instrument['isin'],
            'knowledge_date': knowledge_date,
            'position_type': position_type,
            'effective_date': self.create_effective_date(
                                2, knowledge_date, position_type),
            'account': self.create_account(),
            'qty': self.create_random_integer(),
            'purpose': self.create_purpose(),
            'depot_id': self.create_random_integer(length=5),
            'time_stamp': datetime.now()
        }

        for key, value in self.get_dummy_field_generator():
            record[key] = value

        return record

    def create_purpose(self):
        """ Create a purpose for a depot position

        Returns
        -------
        String
            Depot position purposes are one of Holdings or Seg
        """
        return random.choice(self.DEPOT_POSITION_PURPOSES)
