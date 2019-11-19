from datetime import datetime

from domainobjects.creatable import Creatable


class OrderExecutionFactory(Creatable):
    """ Class to create order executions. Create method will create a
    set amount of executions. """

    def create(self, record_count, start_id):
        """ Create a set number of order executions

        Parameters
        ----------
        record_count : int
            Number of order executions to create
        start_id : int
            Starting id to create from

        Returns
        -------
        List
            Containing 'record_count' order executions
        """

        records = []
        self.instruments = self.retrieve_records('instruments')

        for i in range(start_id, start_id+record_count):
            records.append(self.create_record(i))

        return records

    def create_record(self, id):
        """ Create a single order execution

        Parameters
        ----------
        id : int
            ID of this creation

        Returns
        -------
        dict
            A single order execution object
        """

        instrument = self.get_random_instrument()
        record = {
                'order_id': id,
                'account_num': self.create_random_integer(length=8),
                'direction': self.create_credit_debit(),
                'sto_id': self.create_random_integer(length=7),
                'agent_id': self.create_random_integer(length=7),
                'price': self.create_random_decimal(),
                'currency': self.create_currency(),
                'ric': instrument['ric'],
                'qty': self.create_random_integer(),
                'time_stamp': datetime.now(),
            }

        for key, value in self.get_dummy_field_generator():
            record[key] = value

        return record
