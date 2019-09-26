from domainobjects.generatable import Generatable
from datetime import datetime
import random

class OrderExecution(Generatable):
    """ Class to generate order executions. Generate method will generate a
    set amount of executions. """

    def generate(self, record_count, start_id):
        """ Generate a set number of order executions 
        
        Parameters
        ----------
        record_count : int
            Number of order executions to generate
        start_id : int
            Starting id to generate from

        Returns
        -------
        List
            Containing 'record_count' order executions
        """

        records = []
        self.instruments = self.retrieve_records('instruments')

        for i in range(start_id, start_id+record_count):
            records.append(self.generate_record(i))

        return records

    def generate_record(self, id):
        """ Generate a single order execution

        Parameters
        ----------
        id : int
            ID of this generation

        Returns
        -------
        dict
            A single order execution object
        """

        instrument = self.get_random_instrument()
        return {
                'order_id': id,
                'account_num': self.generate_random_integer(length=8),
                'direction': self.generate_credit_debit(),
                'sto_id': self.generate_random_integer(length=7),
                'agent_id': self.generate_random_integer(length=7),
                'price': self.generate_random_decimal(),
                'curr': self.generate_currency(),
                'ric': instrument['ric'],
                'qty': self.generate_random_integer(),
                'time_stamp': datetime.now(),
            }