from domainobjects.generatable import Generatable
from datetime import datetime
import random

class FrontOfficePosition(Generatable):
    """ Class to generate front office positions. Generate method will
    generate a set amount of positions. Other generation methods included
    where front office positions are the only domain object requiring them. 
    """

    def generate(self, record_count, start_id):
        """ Generate a set number of front office positions 
        
        Parameters
        ----------
        record_count : int
            Number of front office positions to generate
        start_id : int
            Starting id to generate from

        Returns
        -------
        List
            Containing 'record_count' front office positions 
        """

        self.instruments = self.retrieve_records('instruments')

        records = []

        for _ in range(start_id, start_id+record_count):
            instrument = self.get_random_instrument()
            records.append(self.get_record(instrument))
        return records

    def get_record(self, instrument):
        """ Generate a single front office position

        Parameters
        ----------
        instrument : list
            Dictionary containing a partial record of an instrument, only
            containing information necessary to generate depot positions.

        Returns
        -------
        dict
            A single front office position object
        """
        position_type = self.generate_position_type()
        knowledge_date = self.generate_knowledge_date()
        return {
            'ric': instrument['ric'],
            'position_type': position_type,
            'knowledge_date': knowledge_date,
            'effective_date': self.generate_effective_date(
                                0, knowledge_date, position_type),
            'account': self.generate_account(),
            'direction': self.generate_credit_debit(),
            'qty': self.generate_random_integer(),
            'purpose': self.generate_purpose(),
            'time_stamp': datetime.now()
        }

    def generate_purpose(self):
        """ Generate a purpose for a front office position 

        Returns
        -------
        String
            Front office position purposes are always outright
        """

        return 'Outright'
