import random
from datetime import datetime

from domainobjects.creatable import Creatable


class CashBalanceFactory(Creatable):
    """ Class to create cash balances. Create method will create a set
    amount of balances. Other creation methods included where cash balances
    are the only domain object requiring them. """

    CASH_BALANCE_PURPOSES = ['Cash Balance', 'P&L', 'Fees']

    def create(self, record_count, start_id):
        """ Create a set number of cash balances

        Parameters
        ----------
        record_count : int
            Number of cash balances to create
        start_id : int
            Starting id to create from

        Returns
        -------
        List
            Containing 'record_count' cash balances
        """

        records = []

        for _ in range(start_id, start_id+record_count):
            records.append(self.create_record())

        return records

    def create_record(self):
        """ Create a single cash balance

        Returns
        -------
        dict
            A single cash balance object
        """

        record = {
            'amount': self.create_random_integer(),
            'currency': self.create_currency(),
            'account_num': self.create_random_integer(length=8),
            'purpose': self.create_purpose(),
            'time_stamp': datetime.now(),
        }

        for key, value in self.create_dummy_field_generator():
            record[key] = value

        return record

    def create_purpose(self):
        """ Create a purpose for a cash balance

        Returns
        -------
        String
            One of three possible purposes relevant for cash balances
        """

        return random.choice(self.CASH_BALANCE_PURPOSES)
