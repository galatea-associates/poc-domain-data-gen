from domainobjects.generatable import Generatable
from datetime import datetime
import random

class CashBalance(Generatable):

    def generate(self, record_count, custom_args, start_id):

        records = []

        for _ in range(start_id, start_id+record_count):
            records.append(self.get_record())

        return records

    def get_record(self):
        return {
            'amount': self.generate_random_integer(),
            'curr': self.generate_currency(),
            'account_num': self.generate_random_integer(length=8),
            'purpose': self.generate_purpose(),
            'time_stamp': datetime.now(),
        }

    def generate_purpose(self):
        return random.choice(['Cash Balance', 'P&L', 'Fees'])
