from domainobjects.generatable import Generatable
from datetime import datetime
import random

class CashBalance(Generatable):
    """ Class to generate cash balances. Generate method will generate a set
    amount of balances. Other generation methods included where cash balances
    are the only domain object requiring them. """

    CASH_BALANCE_PURPOSES = ['Cash Balance', 'P&L', 'Fees']

    def generate(self, record_count, start_id):
        """ Generate a set number of cash balances

        Parameters
        ----------
        record_count : int
            Number of cash balances to generate
        start_id : int
            Starting id to generate from

        Returns
        -------
        List
            Containing 'record_count' cash balances
        """

        records = []

        for _ in range(start_id, start_id+record_count):
            records.append(self.generate_record())

        return records

    def generate_record(self):
        """ Generate a single cash balance

        Returns
        -------
        dict
            A single cash balance object
        """

        return {
            'amount': self.generate_random_integer(),
            'currency': self.generate_currency(),
            'account_num': self.generate_random_integer(length=8),
            'purpose': self.generate_purpose(),
            'time_stamp': datetime.now(),
        }

    def generate_purpose(self):
        """ Generate a purpose for a cash balance

        Returns
        -------
        String
            One of three possible purposes relevant for cash balances
        """

        return random.choice(self.CASH_BALANCE_PURPOSES)
